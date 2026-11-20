---
title: "linux特殊权限suid,sgid,sbit"
date: 2024-11-13T00:00:00+08:00
draft: false
slug: linux-special-permissions
tags: [Linux]
source: "02-Knowledge/Linux/linux特殊权限suid,sgid,sbit.md"
---
## 特殊权限介绍
### SUID
set user id
当一个可执行文件设置了suid位时，运行该程序的权限变为该文件的所属用户权限
一个经典的案例是`/bin/passwd`
### SGID
set group id
当一个可执行文件设置了sgid位时，运行该程序的权限变为该文件所属组的权限
当一个目录设置了sgid位时，该目录下创建的所有文件和目录的所属组会继承该目录
### SBIT
当一个目录设置了sbit位时，该目录下的文件只有文件所有者才能删除
一个经典的案例是`/tmp`
sbit会被经常用于共享目录
## 如何设置
### suid
```shell
# 方式1
chmod 4755 xx.sh
# 方式2
chmod u+s xx.sh
```
### sgid
```shell
# 方式1
chmod 2755 xx.sh
# 方式2
chmod g+s xx.sh
```
### sbit
```shell
# 方式1
chmod 1666 xx
# 方式2
chmod o+t xx
```
## 应用场景
### 团队协作创建公用目录sgid实现
团队协作中，多个用户在同一用户组中。
团队成员在创建文件或目录时均会继承同一组，避免了文件所属组出现混乱的情况。
```shell
mkdir projects
chown manager:project_team projects
chmod 2755 projects
```
## 参考
book: 鸟哥的linux私房菜