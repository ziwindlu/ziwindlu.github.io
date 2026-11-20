---
title: gitlab私有托管平台搭建
date: 2026-04-03T00:00:00+08:00
draft: false
slug: gitlab-self-hosted
tags: [gitlab]
source: 02-Knowledge/编程/gitlab私有托管平台搭建.md
---
## 引子
提交代码一定要先有仓库,俺尝试自己搭建了一个
## 搭建
使用docker-compose搭建
```yaml
services:
gitlab:
image: gitlab/gitlab-ce:17.10.7-ce.0
container_name: gitlab
restart: always
hostname: 'gitlab.test.com'
ports:
'9080:80'
'9443:443'
'9022:22'
volumes:
'$PWD/config:/etc/gitlab'
'$PWD/logs:/var/log/gitlab'
'$PWD/data:/var/opt/gitlab'
shm_size: '256m'
```
查看日志:
```shell
docker logs -f gitlab
```
获取初始密码:
```shell
docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
```
登陆:
账号:root
密码:上一步获取的初始密码
## 参考
[dockerhub gitlab/gitlab-ce](https://hub.docker.com/r/gitlab/gitlab-ce)