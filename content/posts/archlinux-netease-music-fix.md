---
title: 记录archlinux网易云音乐滚挂
date: 2024-04-24T00:00:00+08:00
draft: false
slug: archlinux-netease-music-fix
tags: [Linux, pacman]
source: 04-Solutions/记录archlinux网易云音乐滚挂.md
---
时间: 2023-06-14
版本: netease-cloud-music 1.2.1-7
美好的一天从滚包更新开始，滚完发现网易云音乐打不开了，果断使用terminal看一看输出
## 噩耗来袭
``` shell
[0614/083435.997611:ERROR:nss_util.cc(706)] Error initializing NSS with a persistent database
```
去网易云音乐aur下讨论发现了解决方案，只需要将`nss`这个包回退到3.89.1-1这个版本就好了
## 解决
方案1:手动下载该版本的包并安装
**step1**
在这里可以找到[Arch Linux Archive](https://archive.archlinux.org/packages/)
**step2**
`sudo pacman -U pkg`
> arch仅会保存近一年的历史包，如果要下载更老的需要手动打包
这里想体验一下，选择了手动打包
方案2:手动打包
**step1**
找到打包的源代码
先去到[nss package页面](https://archlinux.org/packages/core/x86_64/nss/)点击SourceFiles，你就会看到熟悉的gitlab页面啦，这时只需要找到对应的版本克隆到本地就好啦
**step2**
手动打包
进入到含有`PKGBUILD`的目录执行命令`makepkg -s`
慢慢等待你就会发现目录下出现了一个`.zst`文件，有了这个文件你就可以手动安装了
**step3**
手动安装`sudo pacman -U`
## 参考
[在archlinux中如何安装老版本软件](https://zhuanlan.zhihu.com/p/260993724)