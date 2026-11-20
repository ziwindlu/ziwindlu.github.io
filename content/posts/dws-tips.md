---
title: dws使用小技巧
date: 2026-05-20T00:00:00+08:00
draft: false
slug: dws-tips
tags: [未分类]
source: 07-Learning/AI/dws使用小技巧.md
---
在没有桌面环境的机器上运行dws需要使用

```
 dws auth login --device  
```

如果报错
```
▶ Step 4: 检查组织 CLI 授权状态...
{
  "error": {
    "category": "auth",
    "code": 2,
    "message": "device authorization failed: 保存 token 失败: save to keychain: exit status 36"
  }
}
```

```
# macos
security unlock-keychain ~/Library/Keychains/login.keychain-db
```