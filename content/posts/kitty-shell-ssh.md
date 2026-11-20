---
title: kitty+shell集成打造强劲的ssh工具
date: 2024-11-12T00:00:00+08:00
draft: false
slug: kitty-shell-ssh
tags: [kitty]
source: 02-Knowledge/常用软件/kitty+shell集成打造强劲的ssh工具.md
---
## 引子
不想额外下载一个软件来进行ssh管理。俺发现俺现在使用的终端，其附带的功能完全可以打造一个ssh工具。
本文通过ssh+kitty实现了以下功能
便捷的ssh连接 快速复制一个ssh链接
文件上传下载 无需拖拽，纯命令上传下载
属于你自己的终端环境 多用户协作下无敌的爽感
## 便捷的连接
在kitty中连接ssh需要使用`kitten ssh username@host`
可以在`.bashrc`中添加
```shell
ssh(){
if [ "$TERM" = "xterm-kitty" ]; then
kitten ssh $*
else
command ssh $*
fi
}
```
### ssh配置
是不是厌倦了每次都输入`ssh username@host`，你是时候使用ssh配置了
用户的ssh配置在`~/.ssh/config`
示例配置
```shell
# 这样会让配置文件显得更有调理
Include ~/.ssh/config.d/*.conf
Host home_pc
HostName 192.168.0.100
User root
Port 22
IdentityFile ~/.ssh/id_ed25519
```
这样就可以使用`ssh home_pc`愉快的连接了
### 复制当前ssh和当前环境变量
需要打开shell集成
```conf
# lunch --cwd=current 会复制当前的环境变量，如果添加了ssh集成，
map kitty_mod+shift+enter launch --cwd=current
```
用法`alt+shift+enter`
## 文件传输
在kitty中使用`kitten transfer`可以进行下载或上传文件
由于命令过于长，俺在bashrc中定义了一个方法，如果传入的第一个文件不存在则认为是上传，存在则是下载
```shell
# kitty upload file
kcp(){
if [ -e $1 ]; then
# 本地不存在有该文件则认为是从本地下载到远程
kitten transfer  $*
return 0
else
# 本地存在该文件则认为是从远程上传到本地
kitten transfer --direction=upload $*
return 0
fi
}
```
用法：
`kcp file1 file2`
## 打造属于你自己的的终端环境
通过kitty配置，为每一个连接到的ssh服务器配置自己熟悉的alias、软件、环境变量。
配置kitty
编辑`~/.config/kitty/ssh.conf`
```shell
# 主机名
hostname ka
# zsh
env ZDOTDIR=$HOME/.kitty
env remote_home=$HOME/.kitty
copy --dest .kitty/.zshrc .zshrc
copy --dest .kitty/.bashrc .bashrc_kitty_remote
# vim
env VIMINIT=source ".kitty/.vimrc"
copy --dest .kitty/.vimrc .vimrc_kitty_remote
```
配置了这个配置文件后，当连接到主机ka时，kitty会自动复制当前主机的zshrc、bashrc和vimrc到主机ka上。而且不会破坏其原有的配置。
## 其他方便的配置
### edit-in-kitty alias
```shell
# kitty edit file
kvim () {
kitten edit-in-kitty $@
}
skvim(){
local file="$1"
if [ ! -e "$file" ]; then
echo "错误: 文件 $file 不存在。"
return 1
fi
local original_permissions
original_permissions=$(stat -c "%a" "$file")
sudo chmod 777 "$file"
kitten edit-in-kitty $file
sudo chmod "$original_permissions" "$file"
}
kvi () {
kitten edit-in-kitty $@
}
```
## 参考
[kitty](https://sw.kovidgoyal.net/kitty/)