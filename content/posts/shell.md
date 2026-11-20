---
title: shell
date: 2026-04-03T00:00:00+08:00
draft: false
slug: shell
tags: [Linux, Shell]
source: 02-Knowledge/Linux/shell.md
---
## 语言规范
## 语法
### 特殊的变量
坏境变量(均为大写)
`PATH`可执行程序的路径
`PWD`当前所在的目录
`SHELL`当前使用的shell
常见变量
`$0`为该脚本本身的名字
`$#`：表示传入参数的个数。
`$@`：表示所有传入的参数（以独立形式显示，每个参数都保留为单独的字符串）
`$*`：表示所有传入的参数（以一个字符串形式显示，所有参数被合并）
### 变量定义
变量定义以及使用
限定符`local`当前作用域
`export`作为环境变量
`name=value`定义
`$name`使用
### 数据类型
shell中的数据类型有整数、字符串、数组、关联数组(bash4.0及以后的特性)
`'`和`"`的区别
`'`字符原始数据，`"`可以解析其中的变量值
数组使用
```shell
fruits=("apple" "banana" "cherry")
echo "First fruit: ${fruits[0]}"
# tostring
echo "All fruit: ${fruits[*]}"
# 列出所有内容
echo "All fruit: ${fruits[@]}"
# *和@两者的去区别可以参考常见变量
# 获取长度
length=${#fruits[@]}
echo $length
# 遍历
for fruit in "${fruits[@]}"; do
echo "Fruit: $fruit"
done
# 添加元素
fruits+=("date")
# 修改元素
fruits[1]="blueberry"
# 删除元素
unset fruits[1]
# 合并两个数组
more_fruits=("kiwi" "melon")
combined=("${fruits[@]}" "${more_fruits[@]}")
echo "Combined fruits: ${combined[@]}"
```
### 运算符
算术：
`expr`(不推荐)
`echo '1+1' | bc`
(推荐)
`$(( a + b ))`
`let x=a+b`
字符串：
`${#var1}`字符串长度
`${str:start:end}`截取字符串
`${str/old/new}`替换字符
### 分支控制
if语法：
```shell
if [ condition ]; then
# commands
elif [ another_condition ]; then
# commands
else
# commands
fi
```
case语法：
```shell
echo "input 0 or 1"
read option
case $option in
0) echo "0" ;;
1) echo "1" ;;
*) echo "error" ;;
esac
```
判断相关:
| 特性 | `[ ]` | `[[ ]]` | 无括号 |
| ---- | ---- | ---- |
| **本质** | `test` 命令 | Bash 内置功能 | 直接执行命令 |
| **支持正则表达式** | 不支持 | 支持 | 取决于命令 |
| **支持逻辑运算符** | 需要使用 `-a` 和 `-o` | 使用 `&&` 和 ` |  |
| **变量双引号要求** | 必须加 | 可省略 | 通常不需要 |
| **安全性** | 较低（易受空值或特殊字符影响） | 高 | 高 |
### 循环控制
for语法:
```shell
for i in $@ ; do
if [[ condition ]]; then
continue
fi
if [[ condition ]]; then
break
fi
# cmmmands
done
```
while语法:
```shell
while [ condition ]; do
# commands
done
```
### 函数
函数定义
```shell
function xx(){
echo "function 1"
}
xxx(){
echo "function 2"
}
```
函数调用
`function_name`
传参
`fun1 var1 var2`
处理参数
```shell
fun(){
echo $1 $2
}
```
### 引入其他文件
`source file`
## 常见场景
### 简单三元运算
`c=${a:-$b}` 如果a未定义则会将b赋值给c
`c=${a:+$b}`如果a被定义则会将b赋值给c
### 参数处理
getops
## 模板
脚本描述
脚本使用方法
参数处理
依赖检查
日志