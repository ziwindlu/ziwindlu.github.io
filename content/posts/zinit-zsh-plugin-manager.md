---
title: zinit高效的zsh插件管理器
date: 2024-11-30T00:00:00+08:00
draft: false
slug: zinit-zsh-plugin-manager
tags: [zinit, zsh]
source: 04-Solutions/zinit高效的zsh插件管理器.md
---
## 引子
心血来潮，更新一下自己的zshrc，之前写的zinit看不懂了。再去重温一下zinit的文档。记录一下以便备忘。本文会重点介绍常用的插件加载方式。也会推荐一些插件
为什么使用zinit？更快，方便管理。
## 安装zinit
俺比较喜欢手动安装，将下面这些放入你的zshrc，source一下zshrc他就会安装啦。
```shell
ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"
[ ! -d $ZINIT_HOME ] && mkdir -p "$(dirname $ZINIT_HOME)"
[ ! -d $ZINIT_HOME/.git ] && git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
source "${ZINIT_HOME}/zinit.zsh"
```
## 插件加载
### 简单的加载load/light
这些插件加载完成后会放到`$ZINIT_HOME/plugins`
```shell
zinit load zdharma-continuum/history-search-multi-word
```
load和light的区别：
light更快，load慢些。load加载的插件可以跟踪也可以卸载，而light不可以
### 文件加载snippet，含oh-my-zsh和Prezto插件加载
这些插件加载完成后会放到`$ZINIT_HOME/snippets`
```shell
# 单个文件
zinit snippet 'https://github.com/robbyrussell/oh-my-zsh/raw/master/plugins/git/git.plugin.zsh'
# 对于 Oh My Zsh 和 Prezto，您以使用 OMZ:: 和 PZT:: 简写
zinit snippet OMZ::plugins/git/git.plugin.zsh
zinit snippet PZT::modules/helper/init.zsh
```
### 使用svn
如果你的插件不是在github中，而是在svn中。那么你可以添加svn关键字
```shell
zinit ice svn
zinit snippet PZT::modules/docker
```
ice是为下面的zinit命令添加参数
### 更多的参数ice
如上面的svn
更多的ice参数请参考wiki
### 作为程序as"programe"
有时候插件以命令的形式存在，这时我们需要使用as"programe"
```shell
zinit ice as"program" cp"httpstat.sh -> httpstat" pick"httpstat"
zinit light b4b4r07/httpstat
```
对于上面的解释:
`cp"httpstat.sh -> httpstat"`将克隆过后的`httpstat.sh`复制为`httpstat`
pick"httpstat"为`httpstat`设置执行权限
### Turbo模式(常用)
使用wait选项，可以使插件延迟加载`!0`意味着将以接近于0s的延迟后加载
```shell
zinit ice wait'!0'
zinit load halfo/lambda-mod-zsh-theme
```
> 俺的很多配置文件也是抄的，想了解更多语法请参考wiki
## 插件推荐
更详细的用法请参考官方文档
### 命令补全
`zsh-users/zsh-autosuggestions`
### 命令高亮
`zdharma-continuum/fast-syntax-highlighting`
### sudo
`OMZP::sudo`
按两次esc就会在当前行开头补上sudo
### vi-mode
`jeffreytse/zsh-vi-mode`
**配置**
```shell
# 让kj作为esc
ZVM_VI_INSERT_ESCAPE_BINDKEY=kj
```
**使用方法**
normal模式下`vv`进入vim编辑当前命令
### zoxide
模糊cd，他会记住你cd过的目录
`ajeetdsouza/zoxide`
使用方法`z x x`
### fzf
模糊搜索
`junegunn/fzf`
**配置**
```shell
# 触发键改为\
export FZF_COMPLETION_TRIGGER='\'
# fzf窗口高度变为当前窗口的40%
export FZF_TMUX_HEIGHT='40%'
```
### fzf-tab
对fzf的增强，支持命令搜索、参数搜索等
`Aloxaf/fzf-tab`
**配置**
```shell
# disable sort when completing `git checkout`
zstyle ':completion:*:git-checkout:*' sort false
# set descriptions format to enable group support
# NOTE: don't use escape sequences (like '%F{red}%d%f') here, fzf-tab will ignore them
zstyle ':completion:*:descriptions' format '[%d]'
# set list-colors to enable filename colorizing
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
# force zsh not to show completion menu, which allows fzf-tab to capture the unambiguous prefix
zstyle ':completion:*' menu no
# preview directory's content with eza when completing cd
zstyle ':fzf-tab:complete:cd:*' fzf-preview 'eza -1 --color=always $realpath'
# custom fzf flags
# NOTE: fzf-tab does not follow FZF_DEFAULT_OPTS by default
zstyle ':fzf-tab:*' fzf-flags --color=fg:1,fg+:2 --bind=tab:accept
# To make fzf-tab follow FZF_DEFAULT_OPTS.
# NOTE: This may lead to unexpected behavior since some flags break this plugin. See Aloxaf/fzf-tab#455.
zstyle ':fzf-tab:*' use-fzf-default-opts yes
# switch group using `<` and `>`
zstyle ':fzf-tab:*' switch-group '<' '>'
```
## 俺的.zshrc
```shell
# 获取系统信息
os=`uname`
my_home=${remote_home:-$HOME}
# 加载zinit{{{
function zinit_setup(){
# 使用zinit
ZINIT_HOME="$my_home/.local/share/zinit/zinit.git"
[ ! -d $ZINIT_HOME ] && mkdir -p "$(dirname $ZINIT_HOME)"
[ ! -d $ZINIT_HOME/.git ] && git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
source "${ZINIT_HOME}/zinit.zsh"
zinit_load_plug
}
# }}}
# 加载zshrc插件{{{
function zinit_load_plug(){
# powerlevel10k{{{
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
POWERLEVEL9K_DISABLE_CONFIGURATION_WIZARD=true
zinit ice depth=1;
zinit light romkatv/powerlevel10k
# }}}
#
# zoxide{{{
zinit ice lucid wait from"gh-r" as"program" \
pick"zoxide/zoxide" \
atload'eval "$(zoxide init zsh)"'
zinit light ajeetdsouza/zoxide
# }}}
#
# fzf{{{
export FZF_COMPLETION_TRIGGER='\'
export FZF_TMUX_HEIGHT='40%'
zinit ice wait silent from"gh-r" as"program"
zinit load junegunn/fzf
#}}}
#
# fzf-tab{{{
# disable sort when completing `git checkout`
zstyle ':completion:*:git-checkout:*' sort false
# set descriptions format to enable group support
# NOTE: don't use escape sequences (like '%F{red}%d%f') here, fzf-tab will ignore them
zstyle ':completion:*:descriptions' format '[%d]'
# set list-colors to enable filename colorizing
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
# force zsh not to show completion menu, which allows fzf-tab to capture the unambiguous prefix
zstyle ':completion:*' menu no
# preview directory's content with eza when completing cd
zstyle ':fzf-tab:complete:cd:*' fzf-preview 'eza -1 --color=always $realpath'
# custom fzf flags
# NOTE: fzf-tab does not follow FZF_DEFAULT_OPTS by default
zstyle ':fzf-tab:*' fzf-flags --color=fg:1,fg+:2 --bind=tab:accept
# To make fzf-tab follow FZF_DEFAULT_OPTS.
# NOTE: This may lead to unexpected behavior since some flags break this plugin. See Aloxaf/fzf-tab#455.
zstyle ':fzf-tab:*' use-fzf-default-opts yes
# switch group using `<` and `>`
zstyle ':fzf-tab:*' switch-group '<' '>'
zinit ice depth=1 wait atload"zicompinit; zicdreplay" silent
zinit load Aloxaf/fzf-tab
# }}}
#
# vim mod{{{
ZVM_VI_INSERT_ESCAPE_BINDKEY=kj
zinit ice depth=1
zinit light jeffreytse/zsh-vi-mode
# }}}
#
# 补全 sudo highlight{{{
zinit wait lucid depth'1' for \
atload"_zsh_autosuggest_start"  zsh-users/zsh-autosuggestions \
OMZP::sudo \
zdharma-continuum/fast-syntax-highlighting
# }}}
#
}
# }}}
# linux键盘绑定{{{
function linux_keybinding(){
# use ctrl+left ctrl+right to move in words
bindkey "^[[1;5C" forward-word
bindkey "^[[1;5D" backward-word
bindkey '^U' backward-kill-line
}
# }}}
# macos键盘绑定{{{
function macos_keybinding(){
}
# }}}
# 加载bashrc{{{
function source_rc(){
if [ ! -z $1 ]; then
[ -f $1 ] && source $1
fi
}
# }}}
if [[  $os == "Darwin" ]]; then
zinit_setup
macos_keybinding
elif [[ $os == "Linux" ]]; then
# 发行版
source /etc/os-release
case $ID in ;
"arch" | "kali" | "centos")
zinit_setup
linux_keybinding
;;
esac
else
echo "unknow os"
fi
source_rc $my_home/.bashrc
```
## 参考
[GitHub zdharma-continuum/zinit: 🌻 Flexible and fast ZSH plugin manager](https://github.com/zdharma-continuum/zinit?tab=readme-ov-file#zinit-wiki)
[Introduction Zinit Wiki](https://zdharma-continuum.github.io/zinit/wiki/INTRODUCTION/)
[Zsh ArchWiki](https://wiki.archlinux.org/title/Zsh)