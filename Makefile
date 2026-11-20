# ziwindlu.github.io —— 本地常用命令
# 全部在站点源码目录（本 Makefile 所在目录）执行。

HUGO    ?= hugo
PORT    ?= 1313
SRC     ?= content-in/blog-posts
TARBALL ?=

.PHONY: help import build preview stop status refresh clean new

help: ## 显示可用命令
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

import: ## 把 content-in/blog-posts 里的文章导入 content/posts（frontmatter 适配 + wikilink/图片处理）
	python3 scripts/import_posts.py --src $(SRC) --out content/posts --static-images static/images

build: ## 构建静态站点到 public/
	$(HUGO) --minify --gc --cleanDestinationDir --logLevel warn
	@echo "产物：$(CURDIR)/public（$$(du -sh public | cut -f1)）"

preview: ## 启动/确认本机常驻预览（127.0.0.1:$(PORT)）
	PORT=$(PORT) scripts/preview.sh start

stop: ## 停止本机预览
	PORT=$(PORT) scripts/preview.sh stop

status: ## 查看预览状态
	PORT=$(PORT) scripts/preview.sh status

refresh: ## 换源重建：make refresh TARBALL=/绝对路径/blog-posts.tar.gz
	@test -n "$(TARBALL)" || { echo "用法: make refresh TARBALL=/绝对路径/blog-posts.tar.gz"; exit 1; }
	@test -f "$(TARBALL)" || { echo "!! 找不到 $(TARBALL)"; exit 1; }
	rm -rf content-in/blog-posts
	mkdir -p content-in
	tar -xzf "$(TARBALL)" -C content-in
	$(MAKE) import
	$(MAKE) build
	PORT=$(PORT) scripts/preview.sh restart

clean: ## 清掉构建产物（不动文章）
	rm -rf public resources .hugo_build.lock

new: ## 新增一篇文章：make new SLUG=my-post
	@test -n "$(SLUG)" || { echo "用法: make new SLUG=my-post"; exit 1; }
	hugo new content posts/$(SLUG).md
