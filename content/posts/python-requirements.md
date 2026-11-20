---
title: python使用requirements管理依赖
date: 2024-04-24T00:00:00+08:00
draft: false
slug: python-requirements
tags: [Python]
source: 02-Knowledge/编程/python使用requirements管理依赖.md
---
## 引子
写了个python工具，其中用了一些依赖，不想要手动整理依赖放到requests.txt中。俺想到肯定有懒人用法，于是有了今天的文章。使用`pipreqs`来管理
## 安装
```shell
pip install pipreqs
```
## 用法
一步搞定
```shell
pipreqs /path/to/project
```
这样就生成了一个`requirements.txt`啦
## 通过requirements.txt安装依赖
```shell
pip install -r requirements.txt
```
## 参考
id:: 66264e12-b7c5-48bc-b37b-d0fbd31330f0)
[python生成requirements.txt的两种方法 数据驱动 博客园](https://www.cnblogs.com/shun7man/p/14080921.html)