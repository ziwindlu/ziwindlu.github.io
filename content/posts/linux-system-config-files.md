---
title: 一知半解linux系统配置文件
date: 2024-04-24T00:00:00+08:00
draft: false
slug: linux-system-config-files
tags: [未分类]
source: 02-Knowledge/Linux/一知半解linux系统配置文件.md
---
## 关于/etc/fstab
linux系统中用来自动挂载分区使用的
[fstab (简体中文) ArchWiki](https://wiki.archlinux.org/title/Fstab_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))
### 手动编辑
挨个参数对照，仔细一点就可以
### 一键生成脚本
`genfstab -U YourRoot`查看YourRoot中挂载点
其输出可以直接当作`/etc/fstab`文件使用
> `genfstab`在arch-install-scripts这个包中
### 相关命令
`systemctl daemon-reload`重新加载守护程序，这可以让修改的`/etc/fstab`生效
`fdisk -l`查看分区情况
`blkid /dev/sdxx`查看分区uuid
`ls -l /dev/disk/by-uuid/`查看分区uuid
### 添加了新硬盘，在系统启动时自动挂载
现将`/dev/sda2`作为存放虚拟机的目录，让其开机自动挂载到`/home/user/Vbox`下
1. 卸载u盘等非必须开机挂载的设备
2. 挂载该分区`mount /dev/sda2 /home/user/Vbox`
3. 使用脚本写入`/etc/fstab` ，`genfstab -U / > /etc/fstab`
>  踩坑请注意：
不要将tmpfs挂载
不要将tmpfs挂载 
不要将tmpfs挂载
## 设置语言相关的配置文件
### 终端设置中文
当前shell的配置文件，`.bashrc`、`.zshrc`等
### 桌面环境设置中文
`.xprofile`适用于桌面管理器启动的用户
`.xinitrc` 适用于使用 startx 或 SLiM 来启动 X 窗口的用户
`/etc/profile` 所有用户登陆时加载
`/etc/enviroment`此文件linux启动时加载