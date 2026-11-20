---
title: arch挂起配置挂起前后执行脚本
date: 2024-04-24T00:00:00+08:00
draft: false
slug: arch-suspend-hooks
tags: [sleep, power-manager]
source: 02-Knowledge/Linux/arch挂起配置挂起前后执行脚本.md
---
## 引子
装了arch后一直使用的是xfce4-power-manager，这东西只能在超时后自动挂起或休眠。我使用的动态桌面会阻止系统休眠，于是想要使用systemd手动挂起。
手动休眠后没有进行锁屏，还需要配置一些东西，于是有了这篇文章，浅浅的了解了一下arch下的挂起
## 我的环境
DE: i3wm+X11
锁屏: i3lock-color
## 编写挂起前后需要执行的脚本
关于执行该脚本时的传参，详情请看`man systemd-sleep`
```shell
#!/bin/bash
if [ "${1}" == "pre" ]; then
# 挂起或休眠前执行锁屏命令
bash path/shell/lock.sh
elif [ "${1}" == "post" ]; then
# 挂起或休眠唤醒后执行运行动态壁纸的命令
bash path/shell/videoWallpaper.sh
# 其他脚本
bash xxx
fi
```
将该脚本放到`/usr/lib/systemd/system-sleep`目录下
---
title: arch挂起配置-挂起前后执行脚本-de:i3
date: 2024-04-24 23:04:16
updated: 2024-04-24 23:04:23
tags: [sleep,power-manager]
---
## 引子
装了arch后一直使用的是xfce4-power-manager，这东西只能在超时后自动挂起或休眠。我使用的动态桌面会阻止系统休眠，于是想要使用systemd手动挂起。
手动休眠后没有进行锁屏，还需要配置一些东西，于是有了这篇文章，浅浅的了解了一下arch下的挂起
## 我的环境
DE: i3wm+X11
锁屏: i3lock-color
## 编写挂起前后需要执行的脚本
关于执行该脚本时的传参，详情请看`man systemd-sleep`
```shell
#!/bin/bash
if [ "${1}" == "pre" ]; then
# 挂起或休眠前执行锁屏命令
bash path/shell/lock.sh
elif [ "${1}" == "post" ]; then
# 挂起或休眠唤醒后执行运行动态壁纸的命令
bash path/shell/videoWallpaper.sh
# 其他脚本
bash xxx
fi
```
将该脚本放到`/usr/lib/systemd/system-sleep`目录下