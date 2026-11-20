---
title: 记录archlinux滚挂
date: 2024-11-12T00:00:00+08:00
draft: false
slug: archlinux-breakage-recovery
tags: [Linux]
source: 04-Solutions/记录archlinux滚挂.md
---
注意，本篇适用于在pacman升级时\*linux.img丢失的情况
## 原因
使用zinit安装了fzf插件后，fzf的alias与部分命令冲突，导致应用编译会调用到fzf。导致hook执行失败，无法生成\*linux.img
## 解决
找了个ubuntu启动盘启动，chroot后，挂载一些必须挂载的设备
> 随便啥启动盘都可以，可以进入linux环境即可
```shell
# 挂载设备
mount -t proc proc /yourRootMnt/proc/
mount -t sysfs sys /yourRootMnt/sys/
mount -o bind /dev /yourRootMnt/dev/
mount -t devpts pts /yourRootMnt/dev/pts/
```
执行`pacman -S linux`
确保执行完钩子函数，并且生成了\*linux.img
> 一般来说这样就可以了，如果还有问题的话需要更新一下grub.cfg
`grub-mkconfig -o /path/to/grub.cfg`
## 参考
[pacman  Arch Linux 中文维基](https://wiki.archlinuxcn.org/wiki/Pacman#%E5%8D%87%E7%BA%A7%E7%B3%BB%E7%BB%9F%E9%87%8D%E5%90%AF%E5%90%8E%EF%BC%8C%E5%87%BA%E7%8E%B0%22unable_to_find_root_device%22%E9%94%99%E8%AF%AF%EF%BC%8C%E6%97%A0%E6%B3%95%E7%99%BB%E9%99%86)