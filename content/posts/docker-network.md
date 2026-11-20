---
title: docker网络
date: 2026-04-03T00:00:00+08:00
draft: false
slug: docker-network
tags: [Linux, Docker, 网络]
source: 02-Knowledge/Docker/docker网络.md
---
## docker中的网络模式
bridge
host
none
## 相关命令
查看:`docker network ls`,`docker network inspect NETWORK`
创建:`docker network create -d TYPE network_name`
加入:`docker network connect NETWORK CONTAINER [CONTAINERS]`
## 使用
在创建容器时使用`--network `指定网络即可`docker run --network NETWORK IMAGE`