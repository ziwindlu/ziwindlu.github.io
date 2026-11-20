---
title: dns协议
date: 2026-04-03T00:00:00+08:00
draft: false
slug: dns-protocol
tags: [网络, 协议]
source: 02-Knowledge/网络/dns协议.md
---
## dns记录类型 #card #forward
id:: 67a6bca0-b42c-4841-afb1-8543d48c8fd7
**A 记录**：将域名解析为 IPv4 地址。
**AAAA 记录**：将域名解析为 IPv6 地址。
**CNAME 记录**：别名记录，将一个域名映射到另一个域名。
**PTR 记录**：反向解析记录。
**MX 记录**：邮件交换记录，用于电子邮件服务器。
**NS 记录**：指向域名的权威 DNS 服务器。
**SOA 记录**：起始授权机构记录，标识区域的主要信息。
**TXT 记录**：存储任意文本数据，常用于身份验证（如 SPF、DKIM）。
## dns查询模式 #card #forward
id:: 67a6bca0-21f3-48e6-888a-240aa381101a
递归查询
迭代查询
反向查询