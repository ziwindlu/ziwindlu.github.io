---
title: 记录ranger中yank失效的问题
date: 2024-11-30T00:00:00+08:00
draft: false
slug: ranger-yank-fix
tags: [ranger]
source: 04-Solutions/记录ranger中yank失效的问题.md
---
## 引子
ranger用了一会儿发现`yp`没法用了，竟然跟俺报wayland相关的错误，实际上俺用的是x11，闹不清。
那俺就手动改一下吧
## 配置文件修改
修改`~/.config/ranger/rc.conf`。删除原来的映射，添加以下映射
```shell
# 将文件的完整路径复制到剪贴板
map yp shell -f echo -n %d/%f | xclip -selection c
# 将目录路径复制到剪贴板
map yd shell -f echo -n %d | xclip -selection c
# 将文件名（不包括路径）复制到剪贴板
map yn shell -f echo -n %f | xclip -selection c
# 将文件名（不包括路径和扩展名）复制到剪贴板
map y. shell -f echo -n %f | sed 's/\.[^.]*$//' | xclip -selection c
```
## 存在的问题
按理来说，yank是可用的。ranger认为当前环境是wayland指定有问题。这样修改配置文件，会导致x11和wayland不通用。不纠结了，睡大觉