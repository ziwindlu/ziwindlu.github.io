---
title: archlinux下samba服务搭建
date: 2024-04-11T00:00:00+08:00
draft: false
slug: archlinux-samba
tags: [Linux, samba]
source: 02-Knowledge/Linux/archlinux下samba服务搭建.md
---
## 安装所需安装包
`pacman -S samba`
## 修改配置文件
samba没有提供配置文件，需要手动创建。
创建`/etc/samba/smb.conf`文件，内容如下
```smb.conf
# 文件夹名称
[homes]
# 注释
comment = Home Directories
# 共享的路径
path = /home/smb_user/
# 是否显示文件夹
browseable = yes
# 是否可写
writable = yes
```
更多配置项[samba.org](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html)
## 管理smb用户
samba需要linux用户才能使用
修改samba密码
`smbpasswd -a mysmb`
samba管理工具
`pdbedit`
创建用户
`pdbedit -a username`
> 注意这个username是要已经在linux用户中存在的
删除用户
`pdbedit -x username`
查看用户
`pdbedit -L -v`
## 启动服务
`systemctl start smb.service nmb.service`
开机自启动
`systemctl enable smb.service nmb.service`
## 使smb服务可被发现
使smb被linux、mac发现
安装软件包`pacman -S avahi`
启动服务`systemctl start avahi-daemon.service`
使smb被windows发现
安装软件包`yay -S wsdd`
启动服务`systemctl start wsdd.service`
## windows下连接
网络\->映射网络驱动器\->文件夹框内填入`\\ipaddres\homes`\->输入账号密码连接
命令行挂载`net use \\host\share_name password /user:user_name`
## linux下连接
smbclient连接smb`smbclient --user username //host/share_name`
挂载`mount -t cifs -o username=user_name,password=passwd //host/share_name /local_mount_point`
## 参考
[Arch下的KVM win10客户机与宿主机使用samba共享文件的步骤](https://zhuanlan.zhihu.com/p/397145106)
[Samba  Arch Linux 中文维基](https://wiki.archlinuxcn.org/wiki/Samba)