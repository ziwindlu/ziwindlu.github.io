---
title: vim小技巧
date: 2024-04-24T00:00:00+08:00
draft: false
slug: vim-tips
tags: [Vim]
source: 02-Knowledge/Linux/vim小技巧.md
---
## 折叠
`h folding`
### 折叠级别
折叠级别可以理解为折叠深度
### 折叠方式
manual   手工定义折叠
indent   用缩进表示折叠
expr     用表达式来定义折叠
syntax   用语法高亮来定义折叠
diff     对没有更改的文本进行折叠
marker   用标志折叠
### 如何用
| keymap | means                 |
|--------|-----------------------|
| zA     | 递归打开/关闭一个折叠 |
| za     | 打开/关闭一个折叠     |
| zC     | 递归关闭折叠          |
| zO     | 递归打开折叠          |
| zF     | 建立折叠(NzF)         |
| zf     | 建立折叠(zf{motion})  |
| zD     | 递归删除折叠          |
| zR     | 设置折叠等级为最大    |
| zr     | 增加折叠等级          |
| zM     | 设置折叠等级为最小    |
| zN     | 恢复预设折叠等级      |
> 其中zc,zd,zo,zm未写出，对比zA和zR相信你应该也明白其中的意思啦
### 配置
```vim
set foldenable
set foldmethod=marker
set foldcolumn=2
```
## vim在两个窗口中对两个缓冲区中进行比较
在两个窗口中打开两个缓冲区(同一vim进程)
开启比较`:windo diffthis`
关闭比较`:diffoff`
## buffer
新建一个buffer水平分屏,`:new`
新建一个buffer垂直分屏,`:vnew`
## vim中跳转
`ctrl-o` 向前跳转
`ctrl-i` 向后跳转