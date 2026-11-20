---
title: gotour
date: 2026-04-03T00:00:00+08:00
draft: false
slug: go-tour
tags: [Go, 编程语言]
source: 02-Knowledge/编程/gotour.md
---
## 概念
### 包
go从main包开始运行
**声明包**
```go
package main
```
**导入包**
通常你不需要自己导入包，写代码时编辑器会帮你导入
```go
import "fmt"
import (
"fmt"
"math"
)
```
**导出名**
导入一个包时只能使用其中已导出的导出名
当一个导出名以大写字母开头，那么这个导出名就是已导出的
## 语法
### 方法
#### 定义方法
必须定义入参类型和返回类型。
长得和py中的类似，方法要用开头小写的驼峰来命名
``` go
func myFn(add1 int, add2 int) int {
return add2 + add1
}
```
#### 便捷写法
如果参数的类型相同，并且挨在一起，那么可以这样写
```go
func myFn1(add1, add2 int) int {
return add2 + add1
}
```
多个返回值
声明多个返回值使用`(type1, type2)`，接收多个返回值要使用`:=`
```shell
func sw(s1, s2 string) (string, string) {
return s2, s1
}
func main() {
a, b := sw("hello", "world")
t, _ := sw("hello", "world")
fmt.Print(t)
fmt.Println(a, b)
}
```
如果你只想接收一个，也必须使用`:=`，不想保存的参数使用`_`接收
更快捷的返回
使用变量名进行返回
```go
func split(sum int) (x, y int) {
x = sum * 4 / 9
y = sum - x
return
}
```
### 变量
无论使用`var xx type`显式的表示还是自动推导，一个变量是必须有类型的。
#### 定义
使用`var`来定义变量
```go
var abc = "abc"
fmt.Println(abc)
```
如果你在方法内定义了变量，那么必须要使用它
#### 批量初始化
``` go
var a, b, c = 'A', 'B', 'c'
fmt.Println(a, b, c)
```
#### 带类型的变量
```go
var a string
a = "string"
fmt.Println(a)
```
#### 简短的声明
使用`:=`做类型推导
```go
a := "string"
```
#### 常量
使用`const`修饰
```go
const var1 = 123
const (
var2 = 345
var3 = "345"
)
```
### 数据类型
#### go中的数据类型
|类型|标识|默认值|说明|
|---|---|---|---|
|有符号整数|`int,int8,int16,int32,int64`|0||
|无符号整数|`uint,uint8,uint16,uint32,uint64`|0||
|内存地址|`uintptr`|0|实际上是一uint|仅用于存储地址|
|浮点|`float32,float64`|0|浮点数|
|布尔|`bool`|false||
|字节|`byte`|0|`uint8`的别名|
| Unicode 代码点|`rune`|0|`int64`的别名，用于表示单个字符|
|复数|`complex64,complex128`||`complex64`实数部分和虚数部分为`float32`类型|
|字符串|`string`|`""`||
int, uint 和 uintptr 在 32 位系统上通常为 32 位宽，在 64 位系统上则为 64 位宽。
#### 数据类型转换
```go
i = int(13.0)
```
go不会自动做类型转换，需要用户手动进行类型转换
#### 类型推导
变量的类型由右值决定
```go
i := 123
j := i
```
### 循环
#### for基本语法
没有`()`的c的for
```go
for i := 0; i < 10; i++ {
fmt.Println(i)
}
```
#### for的其他特性
可选的初始化语句和后置语句
```go
i := 2
for ;i < 10; {
i++
fmt.Println(i)
}
```
go中没有`++i`，也不能直接将`i++`作为值使用
#### while
for可以不使用前置和后置语句，while在go中就是for
#### 无限循环
```go
for {
fmt.Println("根本停不下来")
}
```
#### 条件
#### if基本语法
没有`()`的c的if
```go
if  1 == 1 {
fmt.Println("b")
}
```
#### if的其他特性
初始化语句，这个初始化语句初始化的变量仅会在当前if内有效
```go
if  b := 12;1 == 1 {
fmt.Println(b)
}
```
#### switch基本语法
没有`()`的c的switch。当前case下有语句时，go自动帮你做break，switch的值可以是字符串或表达式。同样，switch也支持初始化语句，作用域也是当前switch。
```go
color := "green"
switch rgb := 0x000000; color {
case "green":
fmt.Printf("0x%.6x\n", rgb^0x00FF00)
case "red":
fmt.Printf("0x%.6x\n", rgb^0xFF0000)
case "blue":
fmt.Printf("0x%.6x\n", rgb^0x0000FF)
default:
fmt.Println(rgb)
}
```
#### 优雅的if-else-if-else
使用无条件的switch替换
```go
t := time.Now()
switch {
case t.Hour() < 12:
fmt.Println("Good morning!")
case t.Hour() < 17:
fmt.Println("Good afternoon.")
default:
fmt.Println("Good evening.")
}
```
-