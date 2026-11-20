---
title: 使用nginx做简单服务器认证
date: 2024-04-10T00:00:00+08:00
draft: false
slug: nginx-basic-auth
tags: [nginx, basic]
source: 04-Solutions/使用nginx做简单服务器认证.md
---
## 引子
学习过程中需要用到基本认证的站点进行测试，这里选择自己搭建一个
## 配置nginx
配置认证账号密码
```shell
echo "user:" > /opt/www/auth
openssl passwd -apr1 >> /opt/www/auth
```
nginx配置文件中找一个server块
```conf
location /myauth {
auth_basic "need auth";
auth_basic_user_file /opt/www/auth;
alias /opt/www/html;
index index.html;
}
```
重启nginx访问对应路径即可看到要求认证的窗口啦