# ziwindlu.github.io

`ziwindlu` 的个人技术博客，Hugo 静态站点，部署目标是 GitHub Pages 用户站点
<https://ziwindlu.github.io/>（不绑定自定义域名、没有 `CNAME`）。

- **框架**：Hugo **v0.168.0**（extended）。选它是因为单二进制、不依赖 Node、
  markdown 丢进 `content/posts/` 就能发一篇，构建 100 篇以内只要几百毫秒，
  GitHub Pages 原生支持。
- **主题**：[PaperMod](https://github.com/adityatelange/hugo-PaperMod)（MIT），
  固定在 commit `1181196`（2026-10-25），**已 vendored 到 `themes/PaperMod/`**——
  不用 submodule，克隆下来不联网也能构建。自带深色/浅色跟随系统、文章目录（TOC）、
  代码复制按钮、站内搜索、标签页、RSS、sitemap。
- **语言/时区**：`zh-CN`，`Asia/Shanghai`。

## 目录结构

```
hugo.toml              站点配置（baseURL / 菜单 / PaperMod 参数 / 高亮 / 时区）
themes/PaperMod/       vendored 主题（MIT，含 LICENSE，直接提交在仓库里）
layouts/_partials/post_meta.html  唯一一处主题覆盖：文章页显示「源笔记」路径
content/posts/*.md     文章（一篇一个 markdown，由导入脚本生成）
content/about.md       关于页
content/search.md      站内搜索页（layout: search）
content/posts/_index.md 文章列表页
static/images/         从 Obsidian 附件目录复制过来的图片
static/favicon.svg     站点图标（16/32/apple-touch 都指向它）
scripts/import_posts.py 文章导入 + wikilink/图片处理
scripts/preview.sh     本地常驻预览的 start/stop/restart/status
scripts/daemonize.py   双 fork + setsid，让预览脱离调用方会话
Makefile               常用命令入口
content-in/            原始导出包（不提交，换源重建用）
```

## 本地预览（常驻，只监听 127.0.0.1）

```bash
make preview          # 后台启动，默认 http://127.0.0.1:1313/
make status           # 看状态和 HTTP 码
make stop             # 停止
```

等价的手动命令：

`scripts/preview.sh` 内部通过 `scripts/daemonize.py`（双 fork + setsid）启动，服务跑在
独立会话里，调用方的 shell / agent run 退出不会把它一起带走。手写等价命令：

```bash
python3 scripts/daemonize.py --pidfile .preview/hugo.pid --log .preview/hugo.log -- \
  hugo server --bind 127.0.0.1 --port 1313 --baseURL http://127.0.0.1:1313/ \
    --appendPort=false --renderToMemory --disableFastRender --logLevel warn
```

> `--baseURL` 必须显式给：PaperMod 的菜单/文章链接是绝对地址，不指定的话
> 本地预览会链到 `http://localhost/`（没有端口），点了会打不开。

- 日志：`.preview/hugo.log`，PID：`.preview/hugo.pid`
- 端口被占用时 `scripts/preview.sh` 会自动往上找空闲端口（1314、1315…），
  也可以 `make preview PORT=4321` 指定。
- 这是**长驻进程**，不归 Multica daemon 保活；机器重启后需要重新 `make preview`。

## 构建

```bash
make build            # 等价于 hugo --minify --gc --cleanDestinationDir
```

- 产物目录：`public/`（96 篇文章时约 24 MB，其中图片 20 MB）
- 检查点：`public/index.html` 存在，`public/posts/<slug>/index.html` 每篇一个。

## 新增一篇文章

两种方式，任选：

1. **手写**：`make new SLUG=my-post` 生成 `content/posts/my-post.md`，填 frontmatter 后
   `git add` 提交即可。`draft: true` 的文章不会出现在站点上。
2. **从 Obsidian 导入**：把导出的 `blog-posts.tar.gz` 放进来，跑 `make refresh`（见下节）。

frontmatter 必填字段：

| 字段 | 说明 |
| --- | --- |
| `title` | 文章标题 |
| `date` | RFC3339，如 `2026-04-03T00:00:00+08:00` |
| `draft` | `false` 才会发布 |
| `slug` | URL 里的名字，`/posts/<slug>/` |
| `tags` | 字符串数组，如 `["Python", "编程语言"]` |
| `source` | 源笔记在 Obsidian 库里的相对路径（文章页底部会显示） |

本地确认：`make preview` 后打开 <http://127.0.0.1:1313/posts/>，或直接访问
`http://127.0.0.1:1313/posts/<slug>/`。

## 换源重建（第二批文章进来时）

```bash
# 1) 从 issue 评论里拿到新的 blog-posts.tar.gz 附件并下载
multica issue comment list <issue-id> --output json        # 找 attachment id
multica attachment download <attachment-id> -o ./content-in

# 2) 一条命令重建：解包 → 导入 → 构建 → 重启预览
make refresh TARBALL="$PWD/content-in/blog-posts.tar.gz"
```

`make refresh` 会：清空 `content-in/blog-posts/` → 解包 → 重新生成 `content/posts/`
（旧文章被删掉、新文章加进来）→ 重新构建 `public/` → 重启本地预览。

导入规则（`scripts/import_posts.py`）：

- 标题或文件名命中 `multica` 的整篇跳过（用户明确不要 Multica 主题）；
- `index.md` 这类清单文件跳过；
- `[[wikilink]]`：能对上已收录文章的转成站内链接，对不上的降级为纯文本，
  代码块里的 `[[ ... ]]`（Shell 语法）原样保留；
- `![](...)` 图片：从 Obsidian 库的附件目录取同名文件复制到 `static/images/`，
  正文里改写成 `/images/<文件名>`；库里也找不到时降级为一行文字说明，不留死链；
- 只改路径和链接，不改写正文。

## 升级 / 换主题

主题是 vendored 的一份拷贝，升级就是替换目录再重建：

```bash
git clone --depth 1 https://github.com/adityatelange/hugo-PaperMod.git /tmp/pm
rsync -a --exclude '.git' /tmp/pm/ themes/PaperMod/
make build && make preview
```

注意：`layouts/_partials/post_meta.html` 是按当前主题版本抄下来改的（只多了一行
「源笔记」），主题升级后如果这个 partial 有改动，需要重新同步一次。
想彻底换主题：把 `themes/` 换成新主题、`hugo.toml` 里的 `theme` 和 `[params]`
按新主题的文档改，其余（content / static / scripts / Makefile）不用动。

## 回滚

`blog/setup` 分支新增的就是这套站点（配置 + 模板 + 96 篇文章 + 配图），没有改动 `main`。按情况选：

```bash
# 只是本地想回到改动前（分支和改动都还在远端，随时能回来）
git checkout main

# 撤销本分支最后一次提交（保留工作区改动）
git reset --soft HEAD~1

# 已经合到主线上想撤销整个上线
git revert -m 1 <merge-commit-sha>

# 只把内容退回到某个旧版本再重建
git checkout <旧的 commit> -- content/ static/images/ && make build && make preview

# 彻底丢掉这个分支
git push origin --delete blog/setup && git branch -D blog/setup
```

## 部署（不在本分支的职责范围）

本仓库只负责产出可部署的站点源码与 `public/`。真正发布到 GitHub Pages（合并到
`main`、配置 Pages 源、验证线上 200）由部署任务执行，见 issue LZFW-32。
要做线上发布时，从 `main` 构建再发布即可：

```bash
git checkout main
hugo --minify --gc --cleanDestinationDir     # 产物在 public/
```
