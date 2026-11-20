---
title: dockercompose升级mysql并保留数据
date: 2024-04-23T00:00:00+08:00
draft: false
slug: docker-compose-upgrade-mysql
tags: [docker]
source: 02-Knowledge/Docker/dockercompose升级mysql并保留数据.md
---
## 引子
跑了漏扫后服务器mysql版本太低需要升级
## 查看数据库数据存储位置
通过`docker-compose.yml`进行判断，数据库文件在哪里
通常有三种情况
创建了数据卷
映射本地目录
docker容器内部
## 数据备份
对于数据卷和本地目录，容器停止后不会被删除，无需进行多余操作
对于docker容器内部数据需要进行备份，转储存sql之类
## 容器升级
修改`docker-compose.yml`中mysql版本为你想要升级的版本
`docker-compose up -d`，启动容器，容器就会被升级了