---
title: 反向代理
date: 2026-04-03T00:00:00+08:00
draft: false
slug: reverse-proxy
tags: [未分类]
source: 02-Knowledge/网络/反向代理.md
---
## what
服务器端部署的代理，代表后端服务器接收客户端请求，并返回结果。
## why
负载均衡：分发流量到多台后端服务器（如Nginx轮询）
安全防护：屏蔽后端架构，防DDoS（如Cloudflare）
SSL终结：统一处理HTTPS加密，减轻后端压力
## how
常用工具：
nginx