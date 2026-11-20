---
title: centos安装docker以及docker-compose
date: 2024-04-10T00:00:00+08:00
draft: false
slug: centos-install-docker-compose
tags: [Linux, docker, docker-compose]
source: 02-Knowledge/Docker/centos安装docker以及docker-compose.md
---
## 引子
centos安装软件实在太麻烦辣，还得添加源，记录下来方便复制
更新: 原来的docker源没法用了，换成了清华的源，接着更新了其几种安装方式
##  正文
### 安装yum官方源docker
docker,yum官方源的docker版本较低
```shell
yum install -y docker
```
### 安装docker\-ce
`docker-ce`为docker的社区版
#### 方法1(使用yum\-utils)
```shell
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
# 这里我们换成清华的源
sed -i 's+https://download.docker.com+https://mirrors.tuna.tsinghua.edu.cn/docker-ce+' /etc/yum.repos.d/docker-ce.repo
sudo yum makecache
yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
#### ~~方法2(手动导入仓库)~~
添加`/etc/yum.repos.d/docker-ce.repo`这个文件
内容为
```file
[docker-ce-stable]
name=Docker CE Stable - $basearch
baseurl=https://download.docker.com/linux/centos/7/$basearch/stable
enabled=1
gpgcheck=1
gpgkey=https://download.docker.com/linux/centos/gpg
[docker-ce-stable-debuginfo]
name=Docker CE Stable - Debuginfo $basearch
baseurl=https://download.docker.com/linux/centos/7/debug-$basearch/stable
enabled=0
gpgcheck=1
gpgkey=https://download.docker.com/linux/centos/gpg
[docker-ce-stable-source]
name=Docker CE Stable - Sources
baseurl=https://download.docker.com/linux/centos/7/source/stable
enabled=0
gpgcheck=1
gpgkey=https://download.docker.com/linux/centos/gpg
```
安装`sudo yum install docker-ce`
#### 方法3脚本安装
以下内容假定
您为 root 用户，或有 sudo 权限，或知道 root 密码；
您系统上有 curl 或 wget
```shell
export DOWNLOAD_URL="https://mirrors.tuna.tsinghua.edu.cn/docker-ce"
# 如您使用 curl
curl -fsSL https://raw.githubusercontent.com/docker/docker-install/master/install.sh | sh
# 如您使用 wget
wget -O- https://raw.githubusercontent.com/docker/docker-install/master/install.sh | sh
```
>  纯copy的官方文档
### 启动
```shell
systemctl enable --now docker
```
### 安装docker\-compose
```shell
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```
### 可能会遇到的问题
### 我先安装了yum官方源的docker，但是我想升级到最新版，在安装docker\-ce的时候遇到了问题
``` shell
ransaction check error:
file /usr/bin/docker from install of docker-ce-cli-1:24.0.2-1.el7.x86_64 conflicts with file from package docker-common-2:1.13.1-209.git7d71120.el7.centos.x86_64
file /usr/bin/dockerd from install of docker-ce-3:24.0.2-1.el7.x86_64 conflicts with file from package docker-common-2:1.13.1-209.git7d71120.el7.centos.x86_64
```
原因是docker\-ce与旧版本docker冲突，你需要卸载旧版本的docker
``` shell
# 卸载旧版本
sudo yum remove docker-common
# 清空残留文件
sudo rm -rf /var/lib/docker
# 重新安装
sudo yum install docker-ce
```
## 参考
[ docker-ce | 镜像站使用帮助 | 清华大学开源软件镜像站 | Tsinghua Open Source Mirror](https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/)