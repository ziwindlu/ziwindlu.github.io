---
title: Macos无法使用接力问题解决
date: 2026-08-18T00:00:00+08:00
draft: false
slug: macos-handoff-fix
tags: [未分类]
source: 04-Solutions/Macos无法使用接力问题解决.md
---
Macos中会出现一些奇奇怪怪的问题导致无法使用AirDrop、接力、剪切板等功能
粗暴一点直接重启相关应用
``` shell
killall pboard        # 本机剪贴板
killall sharingd      # AirDrop / 通用剪贴板 / 接力相关
killall useractivityd # Handoff 活动同步
killall rapportd      # 附近 Apple 设备通信
```