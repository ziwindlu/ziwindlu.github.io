---
title: vim保存录制宏
date: 2024-08-16T00:00:00+08:00
draft: false
slug: vim-save-macro
tags: [blog, Vim]
source: 02-Knowledge/Linux/vim保存录制宏.md
---
## 引子
在使用vim处理文本时会录制很多宏，有时候这些宏可以重复使用，俺决定将这些宏录制并保存下来，方便下次调用
## 正文
### 保存录制宏
使用vim的内置函数将寄存器保存下来`:call writefile([@x],'file')`
`@x`为寄存器名字，`file`为你要保存到的位置
这样只是简单的将寄存器内容保存下来了。
### 使用保存的宏
编辑上一步保存的文件
```vim
let @a = 'content'
```
`content`为寄存器内容
然后加载该文件即可。就可以使用`@a`调用啦
### 更方便的方法
上面的方法存在一些问题，每次都得去修改宏文件内容。于是俺写了个这
```vim
" 将寄存器内容保存下来
function! SaveRegisterToFile()
" 获取用户输入的寄存器名和文件名
let reg = input("Enter the register name: ")
" 如果reg为空则退出
if reg == "" || empty(getreg(reg))
echo "Register is empty"
return
endif
let file = input("Enter the output file name(default: ~/.vim/script/default.vim): ")
if file == ""
let file = "~/.vim/script/default.vim"
endif
let content = printf("let @%s = '%s'", reg, getreg(reg))
call writefile([content], expand(file), 'a')
" 提示用户操作成功
echo "Register content saved to " . file
endfunction
```
使用`SaveRegisterToFile`即可进行交互式保存寄存器，提供了一个默认文件用于保存，并且添加了`let @x = 'xxx'`方便直接加载。
这里并没有对输入的文件做校验。