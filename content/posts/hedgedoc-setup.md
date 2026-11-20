---
title: hedgedoc搭建
date: 2024-04-10T00:00:00+08:00
draft: false
slug: hedgedoc-setup
tags: [hedgedoc]
source: 04-Solutions/hedgedoc搭建.md
---
## 引子
写接口文档时一些小修改要打开编辑器，还要重新发布一板到开发群组里。对于开发者这种懒人(bushi)是非常痛苦的，市面上支持在线编辑的软件有很多，支持markdown的却不多，再加上内部开发，信息过于敏感，尽量避免到公网。故选择了hedgedoc，并将其部署在本地。
## hedgedoc介绍
一个开源的实时协作文本编辑器，提供了内容版本控制功能等功能
本文包含了该服务的简单部署，以及一些部署中的小技巧，并未涉及太复杂的内容，如反向代理、认证方式等配置。不过本文现有的配置仅作为内部使用也足够了
## docker部署
建议结合自己的配置需求进行配置，如何配置详情见[官方文档](https://docs.hedgedoc.org/configuration/)
### 编辑docker\-compose.yml
``` docker-compose.yml
version: '3'
services:
database:
image: postgres:13.4-alpine
environment:
POSTGRES_USER=hedgedoc
POSTGRES_PASSWORD=password
POSTGRES_DB=hedgedoc
volumes:
database:/var/lib/postgresql/data
ports:
"5432:5432"
restart: always
app:
# Make sure to use the latest release from https://hedgedoc.org/latest-release
image: quay.io/hedgedoc/hedgedoc:1.9.8
environment:
CMD_DB_URL=postgres://hedgedoc:password@database:5432/hedgedoc
CMD_PROTOCOL_USESSL=false
CMD_URL_ADDPORT=true
CMD_DOMAIN=your_ip_or_your_domain
CMD_PORT=3000
# 开启了邮箱注册功能
CMD_EMAIL=true
CMD_ALLOW_EMAIL_REGISTER=true
volumes:
uploads:/hedgedoc/public/uploads
ports:
"3000:3000"
restart: always
depends_on:
database
volumes:
database:
uploads:
```
### 运行
`docker-compose up -d`
> 如果在拉取镜像时出现了`missing signature key`这个问题，请使用最新版docker
## 小技巧
### 批量邮箱注册(本地)
下面是一个批量创建账号的shell脚本
前提：
开启了邮箱注册
curl可用
> 注意，这里的账号和密码一经初始化则不可被修改
使用：
`./yourshellscript.sh <accounts_file>`
`accounts_file`为一个存储着账号密码的文件
一个`accounts_file`示例
``` accounts_file
yourmail@mail.com:your_password
yourmail2@mail.com
```
> 本脚本用`:`作为分隔符，如不添加，会使用默认密码
egurl修改为你搭建的url
default_password为默认密码
脚本本体:
``` shell
# this shell scirpt can create some accounts
# dependencies: curl
#!/bin/bash
regurl='your_register_url'
account_file=$1
default_password='your_default_password'
while IFS= read -r line ;do
unset IFS
IFS=":"
account=($line)
unset IFS
if [[ ${#account[@]} -eq 1 ]];then
curl -X POST -d "email=${account[0]}&password=$default_password" $regurl
echo ""
elif [[ ${#account[@]} -eq 2 ]];then
body="email=${account[0]}&password=${account[1]}"
curl -X POST -d $body $regurl
echo ""
fi
done < $account_file
```
> 邮箱一定要写成`xx@xx.xx`的格式，否则会注册不通过
### 邮箱注册(本地)功能开启与关闭
关闭注册功能
将配置文件改为`CMD_EMAIL=false`即可
运行以下命令
``` shell
cd /your/dockercompose/directory
docker-compose down
docker-compose up -d
```
开启改为true，步骤相同就不重复写了
## 参考
[hedgedoc](https://docs.hedgedoc.org/configuration/)