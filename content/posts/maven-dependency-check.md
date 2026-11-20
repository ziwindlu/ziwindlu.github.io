---
title: maven依赖检查
date: 2024-04-10T00:00:00+08:00
draft: false
slug: maven-dependency-check
tags: [Sec]
source: 04-Solutions/maven依赖检查.md
---
## 引子
在idea中编辑maven依赖文件时，发现了很多警告，定眼一看，原来是maven依赖的漏洞。于是决定找一个检查maven依赖的工具，以备不时之需
## 正文
### 命令行
安装
```shell
yay -S dependency-check-cli
```
安装后会提示这个
```shell
Users should be added to the 'dependencycheck' group to be able to perform vulnerability database updates.
```
需要将用户加到`dependencycheck`这个用户组里面去
使用
`dependency-check -h`用法查看
```shell
dependency-check -o . -s x.jar
```
> 注意，命令行工具需主机要对`nvd.nist.gov`访问流畅
### maven插件方式
这里仅介绍一种开箱即用的方式
其他方式请[查看链接](http://jeremylong.github.io/DependencyCheck/dependency-check-maven/index.html)
项目中引入仅生成html
在pom.xml中plugs中添加以下内容
```shell
<plugin>
<groupId>org.owasp</groupId>
<artifactId>dependency-check-maven</artifactId>
<version>8.4.0</version>
<executions>
<execution>
<goals>
<goal>check</goal>
</goals>
</execution>
</executions>
</plugin>
```
添加完成后导入依赖
运行`mvn dependency-check:check`即可在target中找到对应的报告了