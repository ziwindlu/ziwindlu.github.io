---
title: linux常用的系统信息查看命令
date: 2024-11-30T00:00:00+08:00
draft: false
slug: linux-system-info-commands
tags: [sysinfo]
source: 02-Knowledge/Linux/linux常用的系统信息查看命令.md
---
## 引子
俺经常需要查看某个linux操作系统的版本信息，硬件信息，等等，做个备忘
## 版本信息
### 查看操作系统版本
```shell
cat /etc/os-release
```
> 实际上对于不同的发行版，他们可能会有自己的专属版本信息文件，`os-release`很通用，其他的我们不多作介绍了
### 查看内核版本架构等
```shell
uname -a
```
> `uname`提供了一些查看某些内容的参数，我们这里仅介绍了使用`-a`查看所有的
### 检查发行版和版本号
```shell
lsb_release -a
```
> `lsb_release`也提供了一些查看某些内容的参数
## 硬件信息
### 硬件信息
```shell
# list hardware
lshw
```
### cpu
```shell
lscpu
```
### 硬盘(块设备)
```shell
lsblk
```
### 存储空间
```shell
# disk use 慢
du -h
# disk free 快
df -h
```
### 内存
```shell
free -h
```
### pci设备
```shell
lspci
```
### 主板信息
```shell
dmidecode -t baseboard
```
## 网络
### 网卡信息
```shell
ip a
```
### 路由信息
```shell
route -n
```
### arp表
```shell
arp -a
```
## 其他系统信息
### 启动时间
```shell
uptime
```
### 系统日志
```shell
dmesg
```
### 登陆用户
**当前登陆用户**
```shell
w
```
**最后登陆用户**
```shell
last
```
## shell脚本
为了方便查看，俺添加了vim的折叠
```shell
#!/bin/bash
echo "==============================="
echo "       系统版本信息 {{{"
echo "==============================="
echo "操作系统版本："
cat /etc/os-release
echo
echo "内核版本："
uname -r
echo
echo "详细内核信息："
uname -a
echo
echo "发行版信息："
lsb_release -a 2>/dev/null || echo "lsb_release 命令未找到，请安装 lsb-release 包"
echo
echo "}}}"
echo "==============================="
echo "       硬件信息 {{{"
echo "==============================="
echo "CPU 信息："
lscpu
echo
echo "内存信息："
free -h
echo
echo "硬盘信息："
lsblk
echo
echo "磁盘使用情况："
df -h
echo
echo "显卡信息："
lspci | grep -i vga
echo
echo "主板信息："
sudo dmidecode -t baseboard 2>/dev/null || echo "请以 root 权限运行以查看主板信息"
echo
echo "硬件概览："
sudo lshw -short 2>/dev/null || echo "请以 root 权限运行以查看硬件信息"
echo
echo "}}}"
echo "==============================="
echo "       网络信息 {{{"
echo "==============================="
echo "IP 地址："
ip a
echo
echo "路由表信息："
ip route
echo
echo "网络适配器信息："
lspci | grep -i network
echo
echo "测试网络连通性（到 example.com）："
ping -c 4 example.com
echo
echo "}}}"
echo "==============================="
echo "       其他系统信息 {{{"
echo "==============================="
echo "系统启动时间和负载："
uptime
echo
echo "当前登录用户："
w
echo
echo "系统日志（最近 10 行）："
dmesg | tail -n 10
echo
echo "}}}"
echo "==============================="
echo "       驱动和模块信息 {{{"
echo "==============================="
echo "已加载的内核模块："
lsmod
echo
echo "}}}"
echo "==============================="
echo "       脚本运行完成 {{{"
echo "==============================="
echo "完成所有信息收集"
echo "}}}"
```
