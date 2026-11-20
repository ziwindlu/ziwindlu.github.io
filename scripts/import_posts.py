#!/usr/bin/env python3
"""把 Obsidian 导出的 markdown 文章导入 Hugo 内容目录。

它只做「接入」该做的事，不改写正文语义：
  1. 过滤掉排除项（Multica 相关、清单 index.md 本身）；
  2. 规整 frontmatter（title / date / tags / draft / source / slug）；
  3. 把 [[wikilink]] 转成站内链接：能对上已收录文章就转，对不上降级为纯文本，
     永不留坏链；代码块和行内代码里的 [[...]] 一律不动（Shell 的 [[ ]] 语法）；
  4. 把 Obsidian 的 ![](../assets/xxx.png) 图片复制到 static/images 并改写成 /images/xxx.png。

用法：
  python3 scripts/import_posts.py --src content-in/blog-posts --out content/posts
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import unicodedata
from pathlib import Path

# --------------------------------------------------------------------------- #
# 配置
# --------------------------------------------------------------------------- #

# 标题/文件名命中这些词的整篇跳过（用户明确不要 Multica 主题）
EXCLUDE_PATTERNS = [re.compile(r"multica", re.IGNORECASE)]

# 这些文件名不是文章，是清单
INDEX_FILENAMES = {"index.md", "readme.md"}

FENCE_RE = re.compile(r"^\s*(```|~~~)")
WIKILINK_RE = re.compile(r"\[\[([^\[\]\n]{1,300}?)\]\]")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")


# --------------------------------------------------------------------------- #
# frontmatter 解析（只支持 Hugo 站点用到的形状，避免依赖 PyYAML）
# --------------------------------------------------------------------------- #

def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not m:
        return {}, text
    raw = m.group(1)
    body = text[m.end():]
    return parse_yaml_subset(raw), body


def parse_yaml_subset(raw: str) -> dict:
    data: dict = {}
    current_key = None
    current_list: list | None = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # 列表项归属于上一个 key
        item = re.match(r"^\s*-\s+(.*)$", line)
        if item and current_key is not None:
            value = item.group(1).strip().strip("\"'")
            if current_list is None:
                current_list = []
                data[current_key] = current_list
            current_list.append(value)
            continue
        kv = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if not kv:
            continue
        key, value = kv.group(1), kv.group(2).strip()
        current_key, current_list = key, None
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [v.strip().strip("\"'") for v in inner.split(",") if v.strip()] if inner else []
        elif value.startswith('"') and value.endswith('"'):
            data[key] = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            data[key] = value[1:-1]
        elif value == "":
            data[key] = []
        else:
            data[key] = value
    # 空值列表修正
    for k, v in list(data.items()):
        if v == []:
            data[k] = []
    return data


def yaml_scalar(value: str) -> str:
    """输出安全的 YAML 标量。"""
    s = str(value)
    if s == "" or re.search(r"[:#\[\]{}&*!|>'\"%@`,]", s) or s.strip() != s:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def normalize_date(value: str, fallback: str) -> str:
    """把 2026-04-03 / 2026/04/03 / ISO 时间统一成 RFC3339（+08:00）。"""
    if not value:
        return fallback
    m = re.search(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", str(value))
    if not m:
        return fallback
    y, mo, d = m.group(1), int(m.group(2)), int(m.group(3))
    return f"{y}-{mo:02d}-{d:02d}T00:00:00+08:00"


# --------------------------------------------------------------------------- #
# 链接与图片
# --------------------------------------------------------------------------- #

def norm_key(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).strip()
    return re.sub(r"\s+", " ", text).casefold()


def apply_outside_code(text: str, fn) -> str:
    """只在围栏代码块之外应用 fn（围栏内的行原样保留）。"""
    out: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines(keepends=True):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
                out.append(line)
                continue
            if marker == fence_marker:
                in_fence = False
                fence_marker = ""
                out.append(line)
                continue
        out.append(line if in_fence else fn(line))
    return "".join(out)


def apply_outside_inline_code(text: str, fn) -> str:
    """保留行内代码 `...`，只处理其余片段。"""
    parts: list[str] = []
    pos = 0
    for m in INLINE_CODE_RE.finditer(text):
        parts.append(fn(text[pos:m.start()]))
        parts.append(m.group(0))
        pos = m.end()
    parts.append(fn(text[pos:]))
    return "".join(parts)


def convert_wikilinks(text: str, resolver, stats: dict) -> str:
    def replace_in_segment(segment: str) -> str:
        def repl(m: re.Match) -> str:
            inner = m.group(1).strip()
            if not inner:
                return m.group(0)
            target, _, alias = inner.partition("|")
            target = target.strip()
            alias = alias.strip()
            anchor = ""
            if "#" in target:
                target, _, anchor = target.partition("#")
                target = target.strip()
            if not target:
                return alias or m.group(0)
            href = resolver(target)
            label = alias or target
            if href is None:
                stats["unresolved"] += 1
                stats["unresolved_items"].append(alias or target)
                return label
            if anchor:
                href = f"{href}#{quote_anchor(anchor)}"
            stats["resolved"] += 1
            return f"[{label}]({href})"
        return WIKILINK_RE.sub(repl, segment)

    def line_fn(line: str) -> str:
        return apply_outside_inline_code(line, replace_in_segment)

    return apply_outside_code(text, line_fn)


def quote_anchor(anchor: str) -> str:
    anchor = anchor.strip()
    # Hugo/Goldmark 对中文标题的 id 基本是原文，# 里出现空格时转成 -
    return anchor.replace(" ", "-")


def rewrite_images(text: str, assets_dir: Path, static_images_dir: Path, web_prefix: str,
                   stats: dict) -> str:
    def replace_in_segment(segment: str) -> str:
        def repl(m: re.Match) -> str:
            alt, path = m.group(1), m.group(2)
            if re.match(r"^(https?:|data:|/)", path):
                return m.group(0)
            name = Path(path).name
            dest = static_images_dir / name
            source = assets_dir / name
            if source.is_file():
                if not dest.exists() or dest.stat().st_size != source.stat().st_size:
                    static_images_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, dest)
                stats["images_copied"] += 1
                return f"![{alt}]({web_prefix}/{name})"
            # 没接 Obsidian 库时，仓库里已经落地的图片照样能引用（重建不依赖本机库）
            if dest.is_file():
                stats["images_cached"] += 1
                return f"![{alt}]({web_prefix}/{name})"
            stats["images_missing"].append(path)
            return f"*（图片缺失：{name}）*"

        return IMAGE_RE.sub(repl, segment)

    def line_fn(line: str) -> str:
        return apply_outside_inline_code(line, replace_in_segment)

    return apply_outside_code(text, line_fn)


# --------------------------------------------------------------------------- #
# 主流程
# --------------------------------------------------------------------------- #

def build_resolver(records: list[dict]):
    index: dict[str, str] = {}
    for rec in records:
        href = f"/posts/{rec['slug']}/"
        for key in (rec["title"], rec["slug"], Path(rec["source"]).stem):
            if key:
                index.setdefault(norm_key(key), href)
    return lambda target: index.get(norm_key(target))


def main() -> int:
    ap = argparse.ArgumentParser(description="导入 Obsidian 导出的文章到 Hugo content/posts")
    ap.add_argument("--src", default="content-in/blog-posts", help="导出的 md 目录")
    ap.add_argument("--out", default="content/posts", help="Hugo 内容目录")
    ap.add_argument("--assets", default="/Users/lzf/sync/obsidian/assets",
                    help="Obsidian 附件目录（只读取引用的图片副本）")
    ap.add_argument("--static-images", default="static/images", help="图片落地目录")
    ap.add_argument("--web-prefix", default="/images", help="图片在站点里的 URL 前缀")
    ap.add_argument("--keep", default="", help="逗号分隔的 slug 白名单（调试用）")
    args = ap.parse_args()

    src = Path(args.src)
    if not src.is_dir():
        print(f"!! 找不到源目录：{src}", file=sys.stderr)
        return 2

    assets_dir = Path(args.assets)
    static_images_dir = Path(args.static_images)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(p for p in src.glob("*.md"))
    if not files:
        print(f"!! {src} 里没有 .md 文件", file=sys.stderr)
        return 2

    excluded: list[tuple[str, str]] = []
    stage: list[dict] = []
    for path in files:
        if path.name.lower() in INDEX_FILENAMES:
            excluded.append((path.name, "清单文件，不是文章"))
            continue
        text = path.read_text(encoding="utf-8")
        meta, body = split_frontmatter(text)
        title = str(meta.get("title") or path.stem)
        if any(p.search(title) or p.search(path.stem) for p in EXCLUDE_PATTERNS):
            excluded.append((path.name, f"标题/文件名命中排除规则：{title}"))
            continue
        stage.append({
            "path": path,
            "title": title,
            "slug": path.stem,
            "date": normalize_date(str(meta.get("date") or ""), "1970-01-01T00:00:00+08:00"),
            "tags": [str(t) for t in (meta.get("tags") or [])],
            "source": str(meta.get("source") or ""),
            "body": body,
        })

    keep = {s.strip() for s in args.keep.split(",") if s.strip()}
    if keep:
        stage = [s for s in stage if s["slug"] in keep]

    resolver = build_resolver(stage)
    stats = {"resolved": 0, "unresolved": 0, "unresolved_items": [],
             "images_copied": 0, "images_cached": 0, "images_missing": []}

    imported = []
    for rec in stage:
        body = convert_wikilinks(rec["body"], resolver, stats)
        body = rewrite_images(body, assets_dir, static_images_dir, args.web_prefix, stats)
        tags = ", ".join(yaml_scalar(t) for t in rec["tags"])
        front = (
            "---\n"
            f"title: {yaml_scalar(rec['title'])}\n"
            f"date: {rec['date']}\n"
            "draft: false\n"
            f"slug: {yaml_scalar(rec['slug'])}\n"
            f"tags: [{tags}]\n"
            f"source: {yaml_scalar(rec['source'])}\n"
            "---\n"
        )
        target = out_dir / f"{rec['slug']}.md"
        target.write_text(front + body.lstrip("\n"), encoding="utf-8")
        imported.append(rec)

    # 清理上一次导入留下、这次已不存在的文章（换源重建时保持一致）
    current = {f"{r['slug']}.md" for r in imported}
    removed = []
    for old in out_dir.glob("*.md"):
        if old.name.startswith("_"):
            continue
        if old.name not in current:
            old.unlink()
            removed.append(old.name)

    print(f"导入 {len(imported)} 篇 → {out_dir}")
    print(f"  wikilink：转换 {stats['resolved']} 处，降级为纯文本 {stats['unresolved']} 处")
    if stats["unresolved_items"]:
        sample = sorted(set(stats["unresolved_items"]))[:12]
        print(f"  未收录的内链（已降级）：{', '.join(sample)}")
    cached = len([f for f in static_images_dir.glob('*')]) if static_images_dir.is_dir() else 0
    print(f"  图片：新复制 {stats['images_copied']} 处引用，复用已有 {stats['images_cached']} 处，落地 {cached} 个文件")
    if stats["images_missing"]:
        print(f"  !! 找不到的图片 {len(stats['images_missing'])} 个：{', '.join(sorted(set(stats['images_missing']))[:8])}")
    if removed:
        print(f"  清理旧文章 {len(removed)} 篇：{', '.join(sorted(removed)[:8])}")
    if excluded:
        print(f"跳过 {len(excluded)} 个文件：")
        for name, why in excluded:
            print(f"  - {name}（{why}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
