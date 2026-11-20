---
title: PixelBook2013搞机日记
date: 2024-04-07T00:00:00+08:00
draft: false
slug: pixelbook-2013-modding
tags: [未分类]
source: 06-Life/PixelBook2013搞机日记.md
---
## 引子
无聊逛coolapk刷到了一台pixelbook2013,想都没想直接购入，充值信仰，体验体验chromeOS(没有)
## 配置
鸡鸡配置很低，4+32大内存；CPU是3代i5，低压；触摸屏
花了370大洋淘来的，橙色一般，电池g了，其实是有点亏的。好在卖家刷了bios，系统是fyde os。放家里看电视剧问题不大
## 抛弃fyde os
体验了一段时间fyde os后发现，这鸡鸡带这个系统有点吃力了，南桥发热很严重，只跑了浏览器而已，跑安卓应用更别说了
## 安装arch
arch虽然也反复装了很多次，arch wiki还是要看的，大体步骤记住了，一些小的细节还是容易忘记的
### 制作启动u盘
u盘里装过ventory多系统启动，所以就直接把arch镜像拷到u盘里准备安装。
可能是机器的问题，这个盘启动不了arch，所幸把ventory干掉，直接`cat arch.iso > /dev/sda`，将iso写入u盘
### 本地化
改中文首先要有中文包，在安装arch的时候已经生成过了，没有中文包的话还要取生成一下。更改中文无非就是把环境变量改成zh_CN巴拉巴拉的。为防止tty终端使用中文，请勿将环境变量在`/etc/envirment`或`/etc/profile`中进行设置。
使用`lightdm`等桌面管理器的用户可以在`~/.xprofile`中进行设置，同时建议将语言环境变量也设置在这里
```bash
# set chinese
export LANG=zh_CN.UTF-8
export LANGUAGE=zh_CN:en_US
```
## 参考
[Installation guide (简体中文) ArchWiki](https://wiki.archlinux.org/title/Installation_guide_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))
[archlinux设置中文 | 逐梦](https://0xdadream.github.io/2022/05/17/archlinux-she-zhi-zhong-wen/)