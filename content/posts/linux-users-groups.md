---
title: linux用户和用户组
date: 2026-04-03T00:00:00+08:00
draft: false
slug: linux-users-groups
tags: [Linux]
source: 02-Knowledge/Linux/linux用户和用户组.md
---
## 引子
写文章时用到的很多关于用户和用户组的命令都没有背过，这里记录一下
## 与用户和用户组相关的文件 
|文件| 	作用|
|`/etc/shadow`| 	保存用户安全信息|
|`/etc/passwd`| 	用户账户信息|
|`/etc/gshadow`| 	保存组账号的安全信息|
|`/etc/group`| 	定义用户所属的组|
|`/etc/sudoers`| 	可以运行 sudo 的用户|
| `/home/*` | 	主目录|
>  这些文件有专用的工具进行修改，不要手动修改
## 用户管理
添加用户`useradd -m -aG group1,group2 -s shell username`
|参数|说明|助记|
|---|---|---|
|`-m`| 创建用户家目录|create home|
|`-aG`|添加用户组|append group|
|`-s`|设置shell||
指定用户家目录使用参数`-d /path/to/home username`
禁止用户登陆使用参数`-s /usr/bin/nologin`
删除用户`userdel -r username`
修改用户名`usermod -l newusername oldusername`
修改用户密码`passwd username`
## 用户组管理
查看用户的用户组`groups username`
创建用户组`groupadd groupname`
将用户添加到用户组`gpasswd -a username groupname`
修改组名`gpasswd -n newname oldname`
删除用户组`groupdel groupname`
将用户从用户组中删除`gpasswd -d username groupname`
## 总结
对于用户和用户组的新增和删除均可使用`xxadd`和`xxdel`
对于用户和用户组的的修改使用`xxmod`
## 参考
[用户和用户组  Arch Linux 中文维基](https://wiki.archlinuxcn.org/wiki/%E7%94%A8%E6%88%B7%E5%92%8C%E7%94%A8%E6%88%B7%E7%BB%84#%E7%BE%A4%E7%BB%84%E5%88%97%E8%A1%A8)