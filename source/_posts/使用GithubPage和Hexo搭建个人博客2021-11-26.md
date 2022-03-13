---
title: 使用GithubPage搭建个人博客
date: 2021-11-26 14:00:18
tags: [hexo,git,Linux]
categories: 
	- [上课用]
	- [教程]
---

---

## 搭建前的准备

### 工具以及一些必要的东西

- 一个github账号
- 一台cenos7主机或虚拟机
- ssh工具
  - windows: Xshell 或 openSSH
  - linux: openSSH

> PS:  
> centos安装时为他添加一个用户，并设置为管理员

### Centos与主机建立ssh连接

#### centos网络配置

虚拟机网络模式应为桥接  
dhcp不可用时需要手动配置静态ip  

配置静态ip
[cetnos手动配置ip](https://www.cnblogs.com/yhongji/p/9336247.html)

#### 建立ssh连接

建立ssh连接  
[xshell使用教程](https://cloud.tencent.com/developer/article/1822579)

open ssh的用方法:  
`ssh username@ip`  
其中`username`为centos主机中用户名，当然直接使用root用户也是可以的哈  
ip为`centos`主机的ip地址  

如何查看ip  
{% tabs ip %}

<!--tab windows-->
在**cmd**下输入`ipconfig`
如何进入cmd:  
Win+R  
PS:  
Win+R 意为windows按键+字母R，并非Windows键+大写字母R
<!--endtab-->

<!--tab linux-->
`ip addr` 或者 `ifconfig`
PS  
ifconfig工具在`net-tools`这个包里
<!--endtab-->

{% endtabs %}

> PS:  
> ipconfig和ifconfig有一字之差,不要输错

## 软件安装

---

### ~~yum的使用 本小节弃用~~

**安装软件**  
`yum install applacation -y`
其中`applacation`为软件包的名字  
`-y`意为同意yum的安装决策  

> example:  
> 安装包名为*vim*的软件  
> yum install vim -y

**获取更新**  
`yum update`

**yam源更换**  
yum默认使用centos官方的源，在国内使用较慢
更换为清华源  
[清华源教程](https://mirror.tuna.tsinghua.edu.cn/help/centos/)

---

### nodejs的安装

安装hexo需要nodejs版本不低于10.13  
**Step 1**  
去[nodejs官网](https://nodejs.org/en/download/)中找到适合自己操作系统的包  
使用`wget`将包下载到本地  
使用前要确保`wget`已经安装了  
使用`wget --version`查看是否正确安装  
>以linux amd64的包为例
`wget https://nodejs.org/dist/v16.13.0/node-v16.13.0-linux-x64.tar.xz`

**Step 2**  
解压你刚刚下载的包  
解压tar包需要使用命令`tar`  
**tar命令的使用**  
将name.tar解压到当前目录下：`tar -xvf name.tar`  
将当前目录下dir文件夹中文件压缩到name.tar中：`tar -cvf name.tar dir/`  
> 以刚下载的包为例
`tar -xvf node-v16.13.0-linux-x64.tar.xz`
PS
-v的意为显示压缩或解压缩的细节
-f后要指定tar包

**Step 3**  
添加环境变量  
使用vi或vim编辑器将`PATH=yourBinDir:$PATH`添加到`/etc/prorfile`中
> 这里的yourBinDir要使用绝对目录  
example:
`/home/lbw/nodejs/bin`

**Step 4**  
刷新`/etc/profile`  
有以下两种方法:  

1. `source /etc/profile`
2. 重启`reboot`

**Step 5**  
检查是否正常运作  
`node -v`  
`npm -v`  
如有类似以下回显说明安装成功  

``` bash
[lzf@localhost ~]$ node -v
v16.13.0
[lzf@localhost ~]$ npm -v
8.1.0
```

### 代理软件的安装 可选

为方便管理，这里我们使用v2raya  
[v2raya官网](https://v2raya.org/)  

**v2ray内核安装**  
有以下两种方式:  

1. 根据[v2ray简中介绍](https://github.com/v2fly/fhs-install-v2ray/blob/master/README.zh-Hans-CN.md)安装
2. 使用v2raya官方脚本安装`curl -Ls https://mirrors.v2raya.org/go.sh | sudo bash`推荐

> PS
使用方式2前请检查curl是否已安装
安装curl
`sudo yum install curl -y`

**检查v2ray内核是否安装成功**  
`ls -l /usr/local/bin |grep v2ray`  
有类似以下回显则说明安装成功  

``` bash
ls -l /usr/local/bin |grep v2ray
-rwxr-xr-x. 1 root root 18210816 12月  1 08:14 v2ray
```

**Step 1**  
下载rpm包  
`wget https://github.com/v2rayA/v2rayA/releases/download/v1.5.4/installer_redhat_x64_1.5.4.rpm`
其他操作系统请查看[v2rayA releases](https://github.com/v2rayA/v2rayA/releases)  

**Step 2**  
安装rpm包  
`sudo rpm -i installer_redhat_x64_1.5.4.rpm`

有类似以下回显则说明安装成功  

``` bash
[lzf@localhost ~]$ sudo rpm -i installer_redhat_x64_1.5.4.rpm 
[sudo] lzf 的密码：
******************************
*         Completed!         *
******************************
```

**尝试启动你的v2raya**
`sudo v2raya`  
如有类似以下回显说明启动成功  

``` bash
[lzf@localhost ~]$ sudo v2raya
2021/12/01 08:51:02.453 [A] [main.go:25]  network is connected
2021/12/01 08:51:02.453 [A] [main.go:27]  V2RayLocationAsset is /etc/v2raya
2021/12/01 08:51:02.453 [A] [main.go:27]  V2Ray binary is 
2021/12/01 08:51:02.453 [A] [main.go:27]  v2rayA working directory is /home/lzf
2021/12/01 08:51:02.453 [A] [main.go:27]  v2rayA configuration directory is /etc/v2raya
2021/12/01 08:51:02.453 [A] [main.go:27]  Golang: go1.17.1
2021/12/01 08:51:02.453 [A] [main.go:27]  OS: linux
2021/12/01 08:51:02.453 [A] [main.go:27]  Arch: amd64
2021/12/01 08:51:02.453 [A] [main.go:27]  Lite: false
2021/12/01 08:51:02.453 [A] [main.go:27]  Version: 1.5.4
2021/12/01 08:51:02.453 [A] [main.go:27]  Starting...
2021/12/01 08:51:02.454 [A] [index.go:131]  v2rayA is listening at http://127.0.0.1:2017
```

**访问配置页面**  

- 有DE(Desktop Environment)  
在浏览器中访问127.0.0.1:2017
- 无DE
在局域网另一台电脑上访问该IP:2017

> 如若局域网另一台电脑无法访问配置页面
Centos查看防火墙状态
`sudo systemctl status firewalld`
Centos防火墙关闭
`sudo systemctl stop firewalld`

**将v2raya置于后台运行**  
`sudo systemctl start v2raya`

**v2raya的使用**  
[官方手册](https://v2raya.org/docs/prologue/quick-start/)  

**关于节点**  
自行使用可用工具去google搜索

{% note warning %}
本小节内容仅用作github上传，请勿用作其他用途!!
{% endnote %}

### hexo安装
`npm install -g hexo-cli`

## github设置

{% note info %}
如果你只想做仅在在局域网内可访问的博客的话，这一节可省略
{% endnote %}

### github仓库创建

Create a new repository ->  
填写相关内容：  
Repository name ： yourUserName.github.io  
勾选Public  
勾选Add a README file  
-> Create repository  

### 添加ssh公钥
**生成公钥**  
`ssh-keygen`
全部使用默认选项，生成的公钥在~/.ssh/id_rsa.pub中  
查看公钥并将公钥添加到github

Settings -> SSH and GPG keys -> New SSH key -> 
添加Title 随便
将公钥复制到Key中
-> Add SSH key

### 设置GithubPages

YourRepository -> Settings -> Pages ->
Choose a theme -> 随便选一个 -> Seletct theme ->
Commit changes

> 重新回到Pages页面可查看你的Pages是否创建完成
显示类似如下内容则说明创建完成
Your site is published at <https://YourUserName.github.io>

## 开始搭建

### hexo基本命令介绍

[hexo官方文档](https://hexo.io/zh-cn/docs/)

**新建一个网站**
`hexo init [folder]`

如果没有设置 folder ，Hexo 默认在目前的文件夹建立网站

**新建一篇文章**  
`hexo new [layout] <title>`

[layout]可选，没有的话默认使用_config.yml中的default_layout  
\<title\>必选，文章的名字

**生成静态文件**  
`hexo generate`

可简写为`hexo g`

**启动服务**
`hexo server`

可简写为`hexo s`

### 开始创建你的blog吧

``` bash
mkdir myBlog
cd myBlog
hexo init
```

### 启动你的blog

`hexo clean && hexo g && hexo g`

### 部署到github

**安装hexo-deployer-git** <++>

`npm install hexo-deployer-git --save`

**修改hexo配置文件**  
修改_config.yml底部
example

``` _config.yml
deploy:
  type: git
  repository: yourRepositoryRemoteURL
  branch: main
```

> PS
`yourRepositoryRemoteURL` 在 yourRepository -> Code -> SSH 中复制

**更改GithubPages source分支**  
yourRepository -> Settings -> Pages -> Source
Branch：选择main ,folder 选择/(root) ->
Save

**将静态页面上传到github**  
`hexo clean && hexo g && hexo d`
