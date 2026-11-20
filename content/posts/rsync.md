---
title: rsync强大的文件同步工具
date: 2024-04-10T00:00:00+08:00
draft: false
slug: rsync
tags: [Linux, rsync]
source: 02-Knowledge/常用软件/rsync强大的文件同步工具.md
---
## 引子
备份docker镜像时需要将文件归档复制，留作备忘
## 正文
### rsync常用参数
id:: 65e2c5a5-a39f-4bb2-938a-1f988dc4620d
|参数|说明|助记|
|---|---|---|
|`-a`|已归档模式复制，尽可能保留文件原本的样子|archive|
|`-v`|详情|verbose|
|`-h`|人类可读|human|
|`-n`|模拟执行结果，但不真的这样做||
|`--delete`|添加这个参数会让同步的原目录和目的目录保持相同,即删除目的目录中存在但原目录中不存在的内容||
### 过滤
#### 排除
`--exclude='xxx'`支持正则
#### 包含
`--include='xxx'`必须包含，通常和`--exclude`一起使用
过滤文件过多可以通过`--include-from`和`--exclude-from`指定文件进行过滤
#### 一个正确使用include参数的例子
```shell
rsync -avh --include='include' --include='include/*rc' --exclude='*' .vim/ .vimback
```
> `exclude`要在`include`后面
> 想要包含某个文件下的文件，这个文件也要被包含
### 远程同步
#### ssh
```shell
rsync -avh source_file username@host:dest_file
```
### 增量备份
这会使rsync以`backup_old`为基准将(未修改的文件直接使用这个文件夹中的文件做硬连接到新的文件夹)有改动的文件同步到`backup_new`中
```shell
rsync -avh --delete source_file --link-dest backup_old backup_new
```
### 使用rsync代替mv和cp
在`.bashrc`或`.zshrc`添加以下内容
```shell
if type rsync > /dev/null 2>&1; then
cpr() {
rsync --archive -hh --partial --info=stats1,progress2 --modify-window=1 "$@"
}
mvr() {
rsync --archive -hh --partial --info=stats1,progress2 --modify-window=1 --remove-source-files "$@"
}
fi
```
## 参考
[rsync 用法教程 阮一峰的网络日志](https://www.ruanyifeng.com/blog/2020/08/rsync.html)
[rsync  Arch Linux 中文维基](https://wiki.archlinuxcn.org/wiki/Rsync)