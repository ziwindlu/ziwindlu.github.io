---
title: windows认证
date: 2026-04-03T00:00:00+08:00
draft: false
slug: windows-authentication
tags: [未分类]
source: 07-Learning/笔记/windows认证.md
---
## 一些概念
SAM数据库
Security Accounts Manager
`C:\Windows\System32\config\SAM`
`HKEY_LOCAL_MACHINE\SAM`
SECURITY数据库
`C:\Windows\System32\config\SECURITY`
krbtgt
加入域后创建的用户
LMHash
LAN Manager Hash已被弃用
NTLMHash
NT LAN Manager Hash现在较为常用的，常用于本地认证
netNTLMHash
net NT LAN Manager Hash，基于NTLMHash，更安全。常用于网络认证
## 本地认证
本地用户登陆
本地认证流程
winlogon.exe接收密码
lsass.exe校验传入的密码的hash与sam中的hash对比，相同则认证通过
## 网络认证
质询应答协议，NTLM认证
rdp等远程连接
网络认证流程
c->用户名 ->s
s:校验用户名，通过后，生成challenge(随机16位密码)，并将原用户的NTLMHash与cnalenge生成一个新的密钥并存储在内存中-> challenge ->c
c:将密码的NTLMHash与challenge生成密钥 -> s
s: 对比c与内存中的密钥 -> c
## 域认证
登陆域、访问域中SPN域服务
在域中使用Kerberos认证
kdc 密钥分发中心
as 认证服务
TGT黄金票据
tgs 票据授权服务
ST白银票据
域认证的流程
c想要访问s的服务
c-> username&NTLMHash -> DC:KDC:AS
AS-> TGT -> c
c-> TGT -> DC:KDC:TGS
TGS -> ST -> c
c -> ST -> s