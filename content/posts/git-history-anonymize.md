---
title: git历史提交记录脱敏
date: 2024-04-22T00:00:00+08:00
draft: false
slug: git-history-anonymize
tags: [git, Sec]
source: 04-Solutions/git历史提交记录脱敏.md
---
## 引子
最近写了个小项目，一直放在本地。写简历的时候俺觉得github有点少，于是俺决定将其放到github里去。蛋是，俺发现俺的大名在git的提交记录里面，俺又想保留提交记录，emmmm,于是有了这篇文章，目前仅有对用户名和邮箱的脱敏，因为俺只有这个地方比较敏感。至于代码中提交的系统文件绝对路径，俺倒是不在乎。
## 正文
原本使用`git filter-branch`，尝试运行后提示
```shell
WARNING: git-filter-branch has a glut of gotchas generating mangled history
rewrites.  Hit Ctrl-C before proceeding to abort, then use an
alternative filtering tool such as 'git filter-repo'
(https://github.com/newren/git-filter-repo/) instead.  See the
filter-branch manual page for more details; to squelch this warning,
set FILTER_BRANCH_SQUELCH_WARNING=1.
```
于是俺就去看了看这个项目，本文会使用`git-filter-repo`对提交记录脱敏。
### 安装
pip安装
```shell
pip install git-filter-repo
```
aur安装
```shell
yay -S git-filter-repo
```
### 对邮箱和用户名脱敏
#### mailmap
要对历史记录中的用户名和邮箱进行脱敏，需要用到mailmap文件
mailmap写法
```mailmap
username <email@addre.ss>
<new@ema.il> <old1@ema.il>
newusername <new@ema.il> <old2@ema.il>
newusername <new@ema.il> oldusername<old3@ema.il>
```
修改用户名和邮箱的基础是原邮箱，所有的修改都是建立在匹配原邮箱的基础上做的
#### 使用
编写mailmap文件
```apl
# 注意这个<>是必须的
username <new@ema.il> <email@addre.ss>
```
执行命令
```shell
git filter-repo --mailmap mailmapfile
```
#### 缩写
`--use-mailmap`是`--mailmap .mailmap`的缩写
直接使用当前目录下的`.mailmap`文件
> 如果要将这个文件提交到git中。就使用第一个mailmap写法把，不要将oldemail放到里面了哦
## 参考
[GitHub newren/git-filter-repo: Quickly rewrite git repository history (filter-branch replacement)](https://github.com/newren/git-filter-repo)