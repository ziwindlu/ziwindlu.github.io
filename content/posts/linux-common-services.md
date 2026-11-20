---
title: Linux常用服务
date: 2026-04-03T00:00:00+08:00
draft: false
slug: linux-common-services
tags: [Linux]
source: 02-Knowledge/Linux/Linux常用服务.md
---
## SSH
默认端口22
### 安全配置
禁止密码登陆
```apl
PermitRootLogin no # 禁止root登陆
```
禁止root登陆
```apl
PermitRootLogin prohibit-password  # 仅允许密钥登录
```
端口转发滥用，避免攻击者用作内网渗透
```apl
AllowTcpForwarding no
PermitTunnel no
```
### 如何防御ssh爆破 #card #forward
id:: 67ab4ea1-d4cf-493f-98c3-85b8de165ace
禁用密码登陆
修改默认端口
白名单过滤
配置尝试次数
```apl
MaxAuthTries 3         # 单连接最大认证尝试次数
MaxSessions 2          # 单个IP最大并发会话
LoginGraceTime 30s     # 登录超时时间
```
## SMB
默认端口139,445
windows文件共享
### 安全配置
禁止匿名访问
```apl
guest ok = no
```
控制权限
```apl
write list = user1, user2  # 精确控制
create mask = 0640         # 文件权限限制
```
### 安全漏洞
#### 永恒之蓝 (MS17-010/CVE-2017-0143)
影响版本：Samba 3.x-4.5.9
修复方案：升级smb
### SMBGhost (CVE-2020-0796)
影响版本：Samba 4.3.0-4.11.4
修复方案：升级smb
## FTP
默认端口20,21
文件传输协议
### 安全配置
禁止匿名访问
权限控制
创建文件权限
可进入目录
使用加密传输
### 使用
python快速开启ftp
```shell
python -m pyftpdlib -u user_name -P password -p port --write
```