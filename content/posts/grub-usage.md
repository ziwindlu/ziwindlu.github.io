---
title: grub的使用及使用场景
date: 2024-04-23T00:00:00+08:00
draft: false
slug: grub-usage
tags: [grub]
source: 02-Knowledge/Linux/grub的使用及使用场景.md
---
## 安装软件
一般来说，`grub`或`grub2`会存在于你的系统，如果没有，自行搜索
以arch为例
```bash
sudo pacman -S grub efibootmgr
```
## 安装到硬盘中
### MBR
```bash
grub-install /dev/sda
```
> 这里的sda指硬盘名，而非分区名
> MBR的第一个扇区为引导扇区，所以这里的操作只是把相关代码写到第一个扇区而已
### GPT
```bash
grub-install --target=x86_64-efi --efi-directory=yourEFI --bootloader-id=grub
```
> yourEFI为你当前系统中挂载的efi分区的位置
## 更新引导
```bash
grub-mkconfig -o /grub/grub.cfg
```
> 关于windows：某些发行版可能不识别ntfs分区，需要自行安装软件，方可识别出windows
## 题外话
windows安装时会把所选的efi清空，丝毫不顾及其他系统
## grub主题
grub不一定是黑乎乎的，也是有主题的
### 通用安装步骤
找主题
下载
根据readme安装
重新生成grub.cfg
### 找主题的渠道
github
[GRUB Themes Gnome-look.org](https://www.gnome-look.org/browse?cat=109&ord=latest)
### 主题推荐
[dedsec](https://github.com/VandalByte/dedsec-grub2-theme)
[minegrub](https://github.com/Lxtharia/minegrub-theme.git)
minegrub自定义Mincraft上的字符串
修改`/path/to/minegrub/assets/splashes.txt`这个文件
运行`/path/to/minegrub/splashes.txt`这个文件
你就会发现`/path/to/minegrub/log.png`发生了变化
## 场景:新系统装grub
一般而言，周到的发行版会在安装操作系统时自动进行grub安装，一般不需要用户操作
1. 判断自己硬盘是什么类型(mbr or gpt)
2. 安装软件
3. 根据硬盘的类型选择上面两种装法
4. 更新一下引导
5. 重启
## 场景:grub无了被银币windows顶掉了
在确定是grub被顶掉的情况下按照以下步骤
1. 找到当初装linux的u盘或光盘，插入～
2. 进入发行版提供的体验模式或救援模式
3. 挂载装linux的分区
4. chroot进入挂载的分区
5. 重复场景1
> 进不到grub还有一种可能是直接选择的win启动
## 场景:多系统引导项不全
1. 更新引导
2. 重启
缺少windows:
排查是否为系统无法识别ntfs
黑苹果
1.使用oc引导linux，较新版本的oc已经支持linux引导了
2.grub套娃oc进行引导，需要手动编辑grub.cfg
## 场景:grub g了，进入grub rescue模式 🥵
不要慌，小问题
windows安装时会把所选的efi清空
### grub rescue命令
set查看/设置变量
ls列出分区
insmod
### grub rescue变量
root根目录
prefix`grub.cfg`所在的路径
### 修复
1. 查看那一个分区是linux系统的分区(使用ls进行查看,`ls (hdx,xxx)`可以显示分区类型）
2. 设置变量,`root=(hdx,xxx)`,`prefix=(hdx,xxx)/boot/grub`
3. `insmod normal`
4. `normal`
5. 进入系统
6. 重复场景2
## 其他命令
`update-grub`(一些发行版方便用户使用推出的脚本)
## 踩坑
没事别去PE用DG去分区辣，进系统grub会崩的，老老实实用fdisk吧，图形化工具推荐gparted
## 参考
[自定义GRUB主题zhihu](https://zhuanlan.zhihu.com/p/103866090)
[GRUB (简体中文) ArchWiki](https://wiki.archlinux.org/title/GRUB_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#UEFI_%E7%B3%BB%E7%BB%9F)
[如何使用 GRUB Rescue 修复 Linux](https://cn.linux-console.net/?p=8018)