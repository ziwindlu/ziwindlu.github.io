---
title: fstab开机自动挂载
date: 2024-04-24T00:00:00+08:00
draft: false
slug: fstab-automount
tags: [fstab]
source: 02-Knowledge/Linux/fstab开机自动挂载.md
---
## 引子
双系统下linux和win想共享一块分区，避免每次手动挂载分区，于是看了看fstab
## fstab文件剖析
### 一个实例
```conf
# <file system> <dir> <type> <options> <dump> <pass>
UUID=fed0e3ssr-effe3-4088-9250-ssssssssss	/         	ext4      	rw,relatime	0 1
```
### 字段解析
|概念|说明|举例|
|---|---|---|
|`file system`|文件系统|使用`/dev/sda1`这种格式也可以，uuid格式也可以|
|`dir`| 挂载路径|`/opt`|
|`type`|文件系统类型|`exfat`,`ntfs`等|
|`options`|挂载选项|`rw`,`noexec`|
|`dump`|是否需要备份|通常为0,即不需要|
|`pass`|文件系统检查顺序|root应为1,其他应该大于1|
options
|参数|说明|举例|
|---|---|---|
|`rw,ro`|读写，只读||
|`relatime`| 更新文件访问时间||
|`noatime`| 不更新文件访问时间，提高性能||
|`sync`|同步写入文件系统||
|`noexec`|不允许执行可执行文件||
|`nodev`|不允许创建或使用设备||
|`nosuid`|禁止suid和sgid,防止题全攻击||
> 这里的参数只是一部分
## 实操
## 获取文件uuid
`lsblk -f`
> 实际上，file system可选多种形式，如文件系统标签，gpt分区标签，内核名称等，本文仅使用uuid
### 使fstab立即生效
`systemctl daemon-reload`
`mount -a`
exfat需要额外安装`exfat-utils`
## 参考
[fstab  Arch Linux 中文维基](https://wiki.archlinuxcn.org/wiki/Fstab)