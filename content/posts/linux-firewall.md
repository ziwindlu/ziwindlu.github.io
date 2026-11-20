---
title: Linux防火墙
date: 2026-04-03T00:00:00+08:00
draft: false
slug: linux-firewall
tags: [Linux, 防火墙]
source: 02-Knowledge/Linux/Linux防火墙.md
---
## 基本概念
### 四表table
FILTER表
NAT表
MANGLE表
RAW表
### 五链chain
PREROUTING链
INPUT链
FORWARD链
OUTPUT链
POSTROUTING链
## iptables #card #forward
id:: 67b96abd-426c-46a3-b296-eefb563d0ed0
iptables基于netfilter
### 查看规则
`iptables -t [table]  -L [chain] [options]`
### 添加规则
`iptables -t [table] -A [chain] [match] -j [action]`
### 删除规则
`iptables -t [table] -D [chain]`
### 配置永久规则
`iptables-save > file`保存规则到文件
一般来说iptables会加载`/etc/iptables/*.roules`中的内容
`iptables-restore < file`手动加载规则
## ufw #card #forward
id:: 67b96acf-5566-4be1-9e6a-134afd1b8ae7
ufw基于iptables
### 查看规则
`ufw status [numberd,verbose]`
### 添加规则
`ufw action args`
action:`allow`,`reject`,`deny`,`limit`
简单的args：
端口号/协议`port[/protocol]`
服务名`service`，example:`samba`,`ftp`,`mysql`
默认状态下ufw添加的规则就是永久的
### 删除规则
`ufw delete add_thing`
> `add_thing`为你添加时输入的内容
## firewalld #card #forward
id:: 67b98493-7541-453f-9730-f3db80eb5f35
firewalld是centos默认的防火墙
### 查看规则
`firewall-cmd --list-all`
### 添加规则
`firewall-cmd --add-xx args`
example:
添加http服务放行`firewall-cmd --add-service http`
添加tcp88端口放行`firewall-cmd --add-port 88/tcp`
> 如果想要添加永久规则，需要添加参数`--permanent`，例如`firewall-cmd --permanent --add-service http`，让其生效需要执行`firewall-cmd --reload`
### 删除规则
`firewall-cmd --remove-xx args`
example:
删除服务规则`firewall-cmd --remove-service service_name`