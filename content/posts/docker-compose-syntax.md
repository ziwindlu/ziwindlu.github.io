---
title: docker-compose写法
date: 2026-04-03T00:00:00+08:00
draft: false
slug: docker-compose-syntax
tags: [Linux, Docker]
source: 02-Knowledge/Docker/docker-compose写法.md
---
## 一个标准的yml
```shell
version: '3.9'  # Compose 文件格式版本
services:       # 服务定义
service_name: # 服务名称
image: image_name:tag  # 使用的镜像和标签
build:       # 构建选项（可选）
context: ./path      # Dockerfile 的上下文目录
dockerfile: Dockerfile  # Dockerfile 文件名
container_name: container_name # 容器名称（可选）
ports:        # 端口映射
"外部端口:容器端口"
volumes:      # 数据卷挂载
"宿主路径:容器路径"
environment:  # 环境变量
KEY=value
depends_on:   # 服务依赖关系
other_service_name
networks:     # 网络配置
network_name
networks:         # 自定义网络（可选）
network_name:
driver: bridge
volumes:          # 定义数据卷（可选）
volume_name:
driver: local
```