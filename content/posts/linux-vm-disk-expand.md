---
title: 记录一次linux虚拟机硬盘空间不足扩展硬盘内含docker文件迁移
date: 2024-04-23T00:00:00+08:00
draft: false
slug: linux-vm-disk-expand
tags: [Linux, docker]
source: 04-Solutions/记录一次linux虚拟机硬盘空间不足扩展硬盘内含docker文件迁移.md
---
## 引子
虚拟机硬盘只给了64g，随着服务越来越多，硬盘不够用了
## 分析内存
`ncdu`一个图形化交互式的储存分析工具
`du -sh` disk usage
`df -h` dis free
`du`需要遍历比较慢，可以使用`df`可以粗略的看一下
## 俺的方案
服务器中的绝大部分服务都跑在docker上，决定docker文件单独放到一块硬盘(物理)里。还好有一个习惯，将docker外部存储卷都放到了`/opt`下，所以我只需要将`/opt`和`/var/lib/docker`单独放到一块硬盘中进行存储即可
## 实施过程
这里省略了新硬盘分区，格式化硬盘的操作
强烈建议先备份一下
对`/var/lib/docker`进行迁移
挂载目标硬盘
`mount /dev/sdX1 /mnt`
先停掉docker
`systemctl stop docker`
数据迁移
`rsync -avh /var/lib/docker /mnt/var/lib/docker`
修改docker配置文件
`/etc/docker/daemon.json`
```json
{
"data-root": "/opt/var/lib/docker"
}
```
重启docker
```shell
systemctl daemon-reload
systemctl restart docker
```
对`/opt`进行迁移
数据迁移
`rsync -avh /opt /mnt`
开机自动挂载
修改`/etc/fstab`，添加下面一行
```shell
/dev/sdb1 /opt                       ext4     defaults        0 0
```