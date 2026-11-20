---
title: macmini局域网内远程桌面解决方案
date: 2026-04-03T00:00:00+08:00
draft: false
slug: macmini-lan-remote-desktop
tags: [macos]
source: 04-Solutions/macmini局域网内远程桌面解决方案.md
---
## 引子
macmini到手，临时没有显示器，迫切需要一个远程桌面方案。
macos自带vnc，不过对非mac客户端不友好，不够快，非常卡顿。如果你是mac用户，那么读到这里就可以结束了，用mac自带的远程连接吧，体验极好。
## 效果不好的解决方案
### 网线直连+vnc
俺的mac连接的是无线网，空出来一个网口。vnc卡和网络有关系，于是俺就找了根网线进行直连。
**缺点：**
连接网线太麻烦
效果好了一点，但不多
### rdp
俺尝试安装xrdp，安装成功了，但是无法使用。理论上来说是可以，俺比较菜，怎么弄都不行。
**缺点**
xrdp是运行在x11上的，mac用起来可能比较吃力，因为俺没用上，其他的不作评价
### 安卓平板+airscreen做mac屏幕
ariscreen是商业软件。但是很好用。
非付费用户会在一段时间后断连。
## 最终解决方案
sunshine串流。
### 安装
使用brew直接安装的sunshine是有问题的，需要安装beta版。
### 开机自启
编辑`~/Library/LaunchAgents/sunshine.plist`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-/Apple/DTD PLIST 1.0/EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
<key>Label</key>
<string>home.sunshine</string>
<key>ProgramArguments</key>
<array>
<string>/opt/homebrew/bin/sunshine</string>
</array>
<key>RunAtLoad</key>
<true/>
<key>KeepAlive</key>
<dict>
<key>NetworkState</key>
<true/>
</dict>
</dict>
</plist>
```
### 缺点
linux下moonlight连接时会出现鼠标时不时消失的问题。
## 参考
[GitHub - LizardByte/Sunshine: Self-hosted game stream host for Moonlight.](https://github.com/LizardByte/Sunshine)