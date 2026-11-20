---
title: nginx
date: 2026-04-03T00:00:00+08:00
draft: false
slug: nginx
tags: [Linux, 服务配置]
source: 02-Knowledge/网络/nginx.md
---
## 一个示例配置
基本配置介绍
```conf
# 全局块
user  nginx;
worker_processes  auto;
# 事件块
events {
worker_connections 1024;
}
# http 块
http {
include       mime.types;
default_type  application/octet-stream;
# 日志配置
access_log  /var/log/nginx/access.log;
error_log   /var/log/nginx/error.log;
# 服务器块
server {
listen       80;
server_name  example.com;
# 位置块
location / {
root   /usr/share/nginx/html;
index  index.html index.htm;
}
}
# 还可以有多个 server 块
}
```
## server块
`listen`: 监听的端口
`server_name`: 绑定的域名
`location`: 处理不同请求路径的规则
## 场景
### 反向代理
```conf
server {
listen 80;
server_name example.com;
location / {
proxy_pass http://localhost:3000;
# 这些是推荐加上的可选配置
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
}
}
```