---
title: Linux基础
date: 2026-04-03T00:00:00+08:00
draft: false
slug: linux-basics
tags: [Linux, 系统管理]
source: 02-Knowledge/Linux/Linux基础.md
---
## 文件相关命令
新增:`touch`,`mkdir`
删除:`rm`
修改:`mv`,`cp`
查询:`ls`,`cat`,`find`,`grep`
打包:`tar`,`zip`
## 权限相关命令
基础的三个权限`rwx`
`ls -l`解析
```shell
-rw-r--r--   1 root root       432 Jan 10 13:57  file
```
`-`文件的类型
`rw-`属主权限
`r--`属组权限
`r--`其他用户权限
修改权限:`chmod`
修改属主属组:`chown`
特殊权限:suid,guid,sbit
切换用户:`su` switch user
使用root权限运行命令:`sudo` super user do
## 用户和用户组相关
新增:`useradd`,`groupadd`
删除:`userdel`,`groupdel`
修改:`usermod`,`groupmod`
查询:`/etc/passwd`,`/etc/group`
修改密码:`passwd`
## 网络管理
查看网卡:`ifconfig`,`ip addr`
查看网络连接:`netstat`
## 进程管理
查看进程:`ps`
终结进程:`kill`,`pkill`
其他命令: `top`、`htop`
## 服务管理
`systemd options service_name`
`service service_name options`
`/etc/init.d/service_name options`
## linux运行级别 #card #forward
id:: 67b97041-1b2f-4cea-9b28-bccb786ab85e
|级别|说明|
|---|---|
|0|关机|
|1|单用户模式，用来恢复密码等系统g了时修复|
|2|没有网络的多用户模式|
|3|完整的多用户模式|
|5|图形化多用户模式|
|6|重启|
## 计划任务 #card #forward
id:: 67a6bc9f-66ff-479f-bc75-eac3c3fb41cf
计划任务相关文件:`/etc/crontab`(root用户)
`/var/spool/cron/username`(redhat)
`/var/spool/cron/crontabs/username`(debian)
## 参考
book
鸟哥的linux私房菜