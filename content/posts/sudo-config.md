---
title: sudo命令使用sudoer配置文件解析与实例
date: 2024-11-13T00:00:00+08:00
draft: false
slug: sudo-config
tags: [sudo]
source: 07-Learning/笔记/sudo命令使用sudoer配置文件解析与实例.md
---
## 引子
经常使用sudo命令，但仅限于使用，并没有学习其配置。本文会介绍`/etc/sudoer`文件，和一些常用的配置。
## sudo使用
`sudo -ll`查看当前sudo的配置
`sudo -u username cmd`用户使用username的用户权限运行cmd命令，如果没有`-u`参数会使用root
`sudo -g groupname cmd`用户使用groupname的用户组权限运行cmd命令
## visudo使用
不建议手动修改`/etc/sudoers`文件，建议使用visudo，该命令会在退出时检查`/etc/sudoers`的有效性
visudo默认使用vi编辑器，如果需要使用其他编辑器编辑，需先指定EDITOR变量
`EDITOR=nano visudo`
### 配置
### 较为常用的配置解析
```shell
root ALL=(ALL:ALL) ALL
```
root:用户名或用户组名，当该值为用户组名时，应在前面添加`%`
第一个ALL：该值意味着允许在所有主机上使用sudo命令，在单机环境下这个值无需在意。如果多个主机共享一个sudoers文件，那么这个值可以替换成，ip或hostname
等号后面的(ALL:ALL)：第一个ALL为允许用户或用户组以那个用户权限运行，第二个ALL为允许用户或用户组以那个用户组的权限运行
最后一个ALL：意味可以运行的程序
### alias
```shell
Cmnd_Alias	alias_name=cmd1,cmd2,cmd3
```
不同的用户可能会有相同的命令配置，使用alias可以简化配置文件
### 加载其他配置文件
```shell
@includedir /etc/sudoers.d
```
请注意该文件夹的加载顺序是依靠字母排序的
建议使用`00_filename`此类的文件名
## 常见使用场景
### 允许用户使用sudo时以root权限不输入密码运行一些程序
```sudoers
Cmnd_Alias	NET_CMD=/bin/route,/bin/ip,/usr/bin/ethtool
Cmnd_Alias	VIRT_CMD=/bin/route
Cmnd_Alias	POWER_CMD=/bin/poweroff,/bin/reboot
username localhost=(root:root) NOPASSWD: NET_CMD,POWER_CMD,VIRT_CMD
```
### 仅允许用户使用sudo运行某些程序
```shell
username localhost=/sbin/halt,/sbin/poweroff,/sbin/reboot,/usr/bin/pacman -Syu
```
## 参考
[sudo archwiki](https://wiki.archlinuxcn.org/wiki/Sudo)