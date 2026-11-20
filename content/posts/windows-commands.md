---
title: Windows命令
date: 2026-04-03T00:00:00+08:00
draft: false
slug: windows-commands
tags: [未分类]
source: 02-Knowledge/系统/Windows命令.md
---
## 文件相关 #card #forward
id:: 67b98630-7efd-480f-bbad-4e5e7479e33d
`cd`切换目录，特殊的如果进入其他盘符应该这样`X:`而不是`cd X:`，x为你向进入的盘符
`dir`列出文件，列出隐藏文件`-a`
`type`输出文件内容
`move`移动，重命名文件
`copy`复制文件
`ren`重命名
`findstr`查找内容类似grep
`del`删除
`mkdir`创建目录
`rmdir`删除目录
## 用户和用户组管理 #card #forward
id:: 67a6bca0-f234-42fd-8a5e-c277dc9868aa
### 用户相关操作
**查看用户信息**:`net user [USERNAME]`
**创建新用户**:`net user USERNAME PASSWORD /add`
**删除用户**:`net user USERNAME /delete`
**修改密码**:`net user USERNAME NEW_PASSWORD`
**启用/禁用用户**:`net user USERNAME /active:<yes/no>`
### 用户组相关操作
**查看用户组**，**新建用户组**，**删除用户组**和用户的操作相同，将`net user`改为`net localgroup`即可
**添加用户到用户组**:`net localgroup GROUPNAME USERNAME /add`
**从用户组中删除用户**:`net localgroup GROUPNAME USERNAME /delete`
### 激活administrator
`net user administator active`
## 权限相关 #card #forward
id:: 67b986c4-f71a-49d5-9012-824a945fe568
查看当前用户权限
`whoami /priv`
查看用户详细信息
`whoami /all`
## 网络相关
`netstat -ano`查看网络连接
`ipconfig`网卡信息
## 进程相关 #card #forward
id:: 67b9882e-0bd4-4457-8afe-dc4da64f0ea1
`taskllist`列出进程
`taskkill /pid 1022`关闭进程
## 文件共享 #card #forward
id:: 67b98949-cc31-4bc6-9d95-a2d5ec056b68
`net use`查看文件共享
`net use \\IP地址或主机名 /user:administrator "密码"`创建文件共享
`net use 共享连接名 /del`删除文件共享
## 票据相关 #card #forward
id:: 67c71a77-14cc-4c64-8a26-26bf758f7ed1
`klist`查看票据
`klist purge`清空票据