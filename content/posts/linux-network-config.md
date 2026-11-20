---
title: linux使用配置文件配置网络
date: 2024-11-13T00:00:00+08:00
draft: false
slug: linux-network-config
tags: [Linux]
source: 02-Knowledge/Linux/linux使用配置文件配置网络.md
---
## 引子
对于游走于n个发行版的小卡拉米，时常面临着要使用配置文件配置ip地址的问题。然鹅这些发行版并不统一，大家都自己整自己的，存在一些差异。虽然有很多好用的工具可以用，但是保不齐工作的时候就得用配置文件手动配置。这里记录一下。
## Debian/Ubuntu系列
### 较老一点的版本
网卡配置信息在`/etc/network/interfaces`，这是个文件
配置静态ip
```shell
# 以太网接口 enp3s0 配置
auto enp3s0
iface enp3s0 inet static
address 192.168.1.100
netmask 255.255.255.0
gateway 192.168.1.1
dns-nameservers 8.8.8.8 8.8.4.4
```
### 新一点的版本
网卡配置信息在`/etc/netplan/01-netcfg.yaml`，这是个文件
配置静态ip
```yaml
network:
version: 2
renderer: networkd
ethernets:
enp3s0:
dhcp4: no
addresses:
192.168.1.100/24
gateway4: 192.168.1.1
nameservers:
addresses:
8.8.8.8
8.8.4.4
```
## Arch系列
配置文件在`/etc/netctl`，这是个目录，具体的文件名可以随便写
配置静态ip
```shell
Description='A basic static ethernet connection'
Interface=enp3s0
Connection=ethernet
IP=static
Address=('192.168.1.100/24')
Gateway='192.168.1.1'
DNS=('8.8.8.8' '8.8.4.4')
```
## Red Hat/CentOS系列
网卡配置信息在`/etc/sysconfig/network-scripts/`，这是个目录，具体文件名应为`ifcfg-interfacename`
配置静态ip
```shell
DEVICE=enp3s0
BOOTPROTO=static
ONBOOT=yes
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
DNS2=8.8.4.4
```
## 注意
使用配置文件配置完后，需要重启网络
使用NetworkManager作为网络管理的：
`systemctl restart NetworkManager`
手动：
使用ip命令对对应网卡进行手动重启
`ip link set dev interface down`
`ip link set dev interface up`
## dns配置
这玩意大家竟然出奇的统一，基本都放在`/etc/resolv.conf`
```shell
# /etc/resolv.conf
nameserver 8.8.8.8       # Google DNS
nameserver 8.8.4.4       # Google DNS
```
## 参考
[网络管理 archwiki](https://wiki.archlinuxcn.org/zh-sg/%E7%BD%91%E7%BB%9C%E9%85%8D%E7%BD%AE)