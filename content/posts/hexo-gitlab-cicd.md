---
title: hexo使用gitlab进行cicd
date: 2024-04-24T00:00:00+08:00
draft: false
slug: hexo-gitlab-cicd
tags: [hexo, devops, gitlab]
source: 04-Solutions/hexo使用gitlab进行cicd.md
---
## 引子
由于个人博客过于松散，不想写完就发布到gitpage上，于是做了一个基于gitlab的cicd发布到内网
## .gitlab-ci.yml编写
```yaml
stages:
build
build:
stage: build
before_script:
npm install
export TRIGGER=diff # 指定触发规则  full：全量部署，diff：差异部署，不填：不执行操作
script:
bash deploy
```
## Runner
### Runner安装
[官方教程](https://docs.gitlab.com/runner/install/linux-manually.html)
```shell
# 这里以centos7,x86_64架构做演示
# 下载rpm包并安装
curl -LJO "https://gitlab-runner-downloads.s3.amazonaws.com/latest/rpm/gitlab-runner_amd64.rpm"
rpm -i gitlab-runner_amd64.rpm
```
### hexo环境
``` shell
# hexo本体
npm install -g hexo-cli
# 主题
npm install hexo-theme-butterfly
```
## 自动部署脚本编写
```shell
#!/bin/bash
npx hexo g
# 直接将静态文件覆盖到了runner所在nginx目录
cp public/* /usr/share/nginx/html/ -rf
```