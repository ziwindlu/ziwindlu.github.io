---
title: asciinema记录命令输入输出写作利器
date: 2024-04-23T00:00:00+08:00
draft: false
slug: asciinema-record-terminal
tags: [asciinema]
source: 04-Solutions/asciinema记录命令输入输出写作利器.md
---
## 引子
在记录命令如何使用的时候，时常需要进行记录输入输出，但是每次从终端中复制就很呆，俺就找到了这个命令，非常方便的记录命令的输入和输出。
俺发现了asciinema，该软件可以记录你在终端中的输入输出，输出可导出为gif。
## 安装
```shell
sudo pacman -S asciinema
```
## 用法
```shell
asciinema command [options] [args]
```
## asciinema命令
### rec录制命令
开启录制并保存到`x.cast`中
```shell
asciinema rec x.cast
```
### cat查看命令
查看`x.cast`，注意这个命令只会输出与终端的标准输入与输出，如果进入了vim之类的将不会被记录
```shell
asciinema cat x.cast
```
### play播放命令
播放`x.cast`
```shell
asciinema play x.cast
```
### upload上传你的录像
这个功能俺不经常使用
### 结束记录
`exit`退出或者`ctrl+d`均可
## 常用参数
emmmm 有些参数其实没必要记住，后面我们直接放到配置文件里面
rec命令参数
|参数|说明|举例|
|---|---|---|
|`--stdin`|所有的输入都会被记录，会展出时删除的操作|放到配置文件里了|
|`--append`|在文件后添加|`asciinema rec --append output.cast`|
|`--overwrite`|覆盖原文件||
|`-c`|记录接下来执行的命令|`asciinema -c ls`,放到配置文件里了||
|`-q`|安静的执行|放到配置文件里了||
## 配置
配置文件在`~/.config/asciinema/config`
```conf
[record]
command = /bin/bash -l
stdin = yes
quiet = yes
[play]
speed = 2
pause_key = p
step_key = s
next_marker_key = m
```
## 生成gif
需要安装`agg`或者`asciinema-agg`一个东西，名字不一样
```shell
yay -S asciinema-agg
```
使用方法
```shell
agg x.cast
```
## 将录制文件以text纯文本形式输出，无控制字符
参考了[GitHub asciinema/avt: asciinema virtual terminal](https://github.com/asciinema/avt)
把他克隆下来，运行需要有rust环境和cargo
俺按照原作者的执行方式做，并没有成功，修改了一下`Cargo.toml`这个文件
```toml
[package]
name = "avt"
version = "0.10.3"
edition = "2021"
authors = ["Marcin Kulik <m@ku1ik.com>"]
repository = "https://github.com/asciinema/avt"
description = "asciinema virtual terminal"
license = "Apache-2.0"
[dependencies]
serde = { version = "1.0.130", features = ["derive"] }
rgb = "0.8.33"
unicode-width = "0.1.11"
[dev-dependencies]
rand = "0.7"
proptest = "1.2.0"
criterion = "0.3"
pretty_assertions = "1.0"
[[bench]]
name = "parser"
harness = false
# 这个path是俺本地的，你要改成你本地的
path = "~/git/avt/src/parser.rs"
[[bench]]
name = "vt"
harness = false
# 这个path是俺本地的，你要改成你本地的
path = "~/git/avt/src/vt.rs"
# 这个是后加的,不用在意name
[lib]
name = "test"
path = "~/git/avt/src/lib.rs"
```
> 可能有更好的方法，没玩过rust，这样能用
运行`asciinema cat record.cast | cargo run -q  --example text`就能输出纯文本啦
俺在`.bashrc`中定义了一个方法
```bashrc
# 将asciinema的记录文件转为text
ascii2text(){
# 这里严格来说写的不严谨没有考虑$*的合法性
asciinema cat $* | cargo run -q -p avt --example text
}
```
## 其他
### 编辑你录制的内容
可以使用下面这个工具
[GitHub cirocosta/asciinema-edit: asciinema casts post-production tools](https://github.com/cirocosta/asciinema-edit)
## 参考
[技术|用 Asciinema 记录你的终端会话](https://linux.cn/article-14216-1.html)
[Manual asciinema docs](https://docs.asciinema.org/manual/)
[GitHub asciinema/avt: asciinema virtual terminal](https://github.com/asciinema/avt)
[Extracting Text from the casts or pure text casts without terminal control codes (for written documentation) · asciinema · Discussion #45 · GitHub](https://github.com/orgs/asciinema/discussions/45)