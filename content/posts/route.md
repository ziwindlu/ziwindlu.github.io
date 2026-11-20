---
title: route
date: 2026-04-03T00:00:00+08:00
draft: false
slug: route
tags: [未分类]
source: 02-Knowledge/网络/route.md
---
## what
route是任何网络中选取路径的程序
## why
解决数据从源节点到目标节点的有效传输问题
## how
以linux中ip命令为例
查看路由
```shell
ip route show
```
添加路由
```shell
# 添加默认路由
ip route add default via 192.168.1.1 dev eth0
# 添加静态路由
ip route add 10.0.0.0/8 via 10.0.0.1 dev tun0
```
删除路由
```shell
ip route del 10.0.0.0/8
```
修改路由
```shell
ip route replace 10.0.0.0/8 via 10.0.0.2 dev tun0
```
## 常见问题
### 路由表的种类
直连路由
静态路由
动态路由
默认路由
策略路由