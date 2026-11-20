---
title: hackintosh初体验
date: 2024-04-10T00:00:00+08:00
draft: false
slug: hackintosh-first-try
tags: [macos]
source: 06-Life/hackintosh初体验.md
---
## 引子
入了手一个古老的笔记本，发现配置可以黑苹果。加上人在隔离，无趣，想起之前手撸OC的悲惨经历，决定重来一次。
## 前言
此文章不是专业安装教程，仅为记录搞机日常。
在繁琐的黑苹果过程中，需要摆正心态，善用搜索引擎。降低预期，容忍他的一些小问题。
## 主机配置和驱动问题
戴尔灵越5570
CPU:i5 8250U
GPU:核显(独显无法驱动)
硬盘:
无线网卡:不可用(其实后面俺换了一个可驱动的无线网卡，隔空投送啥的都能用了，但是俺不想写了)
蓝牙: 可用
有线网卡:需加载驱动
> 相信了解黑苹果的朋友都知道硬件的重要性，这里不多赘述
## 收集文件
经历了手撸OC的痛，痛定思痛决定直接使用别人的efi
github中找到的
[stayboogy's efi](https://github.com/stayboogy/Hackintosh_Dell-Inspiron-5570_Catalina)
[Mateo1234454545‘s efi](https://github.com/Mateo1234454545/DELL-5570-Hackintosh)
两个efi都使用过，第二个efi基本完美，可以直接使用，仅需要将OC中的CFGLock相关选项设置为true，甚至bios都不需要修改
生命在于折腾，所以我用了第一个，以下内容基于第一个efi(其实是装了n此最后停留在了1中，不想换了才这样滴)
后续需要2中ACPI，Kexts中文件
## 制作安装u盘
### 镜像下载
需要python环境，使用pyton3
[Making the installer in Linux | OpenCore Install Guide](https://dortania.github.io/OpenCore-Install-Guide/installer-guide/linux-install.html#downloading-macos)
根据efi中的描述，下载对应版本
### 分区
win下使用`DiskGenius`进行分区
Linux下使用`gdisk`(OC官方推荐)
### 镜像的使用和写入
Linux下使用工具`dmg2img`
arch下安装`yay -S dmg2img`
> 如果你的u盘速度堪忧，可能需要多等一会儿
## BIOS设置
### STAT控制器相关
为了防止进入安装程序后找不到硬盘，需要将此项改为AHCI
> 如果更改后你的Windows无法启动，原因是windows没有安装AHCI驱动。
> 解决:
> 将此选项更改为原来的模式，`msconfig`中启用安全启动并应用
> 开机前将此选项再次更改为AHCI
> 进入Windows，查看设备管理器是否更改成功
### 安全启动
禁用此项
### CPU虚拟化
禁用此项
> 安装后可重新开启，以满足使用虚拟机的需求，但是不太好用
### BIOS中无法更改的内容
解决卡logo和卡进度条无限重启问题
**注意，此更改可能会使你的电脑变砖，以下内容仅适合戴尔灵越5570，其他型号主板慎用。且这一步是必须的，修改前请备份BIOS文件。**
1. DVMV PRE-ALLOCATED set to 64MB: setup_var 0x795 0x2
2. DVMT TOTAL GFX MEM set to MAX: setup_var 0x796 0x3
3. CFG Lock set to Disabled: setup_var 0x4ED 0x0
4. I2CO INTERUPT MODE set to GPIO Interrupt : setup_var 0x272 0x0
以上内容为完美黑苹果做准备，至少需要设置1。
如果你只设置了1，需要在OC配置文件中将CFGLOCK相关选项修改为true。
如果不在OC配置文件中将CFGLOCK相关选项修改为true，则需要配置3
> 如果修改后仍无法进入安装界面，请全部修改
#### 修改步骤
**修改前请备份BIOS文件**
选择`/EFI/Boot/BOOTx64.efi`启动。
启动后你会看到熟悉的grub
`setup_var 0x795`查看该值并记录下来
`setup_var 0x795 0x2`将该值更改
重复以上两步，将你需要的内容修改完毕即可重启
### 将u盘设置为启动盘 😁
这是最后一步，也是最重要的一步。
## 安装macOS
### 磁盘分区
可在PE或Windows中分出供mac使用的分区，类型随意，只需规定大小
进入mac安装界面使用磁盘工具将上一步分出的分区格式化为APPLE类型即可
## 系统安装
随便点点就行
> 这一步是需要网络的，安装时间根据网络环境而定
## 引导
将u盘中OC，Boot文件夹复制到WindowsESP分区中的EFI中即可，开机可以检测到windows
> 这步结束后，你就获得了一个黑苹果系统，可黑苹果才刚刚开始，你还需要处理驱动等问题
## 关于OC编辑器
上面的某些步骤可能涉及到OCconfig的编辑，均需要OC编辑器进行修改，足够硬也可以用眼解析文件
常用的OC编辑器
OCC(版本不一致会损毁OCconfig)
OCAT(升级OC方便，不怎么用)
ProperTree(官方推荐)
OCC的版本选择
[更新日志(非官方)](https://macoshome.com/hackintosh/htools/2100.html)
根据日志选择版本，这里我们选择支持OC0.6.1的版本
## 遇到的问题
大部分问题都写在具体的步骤中了，剩下的就是一些完美黑苹果的问题了
### 亮度无法调节
**原因**
efi1中`\ACPI\SSDT-PNLF.aml`文件缺失
可以使用efi2中的`\ACPI\SSDT-PNLF-CFL.aml`
**解决**
将`.aml` 文件复制到`\EFI\OC\ACPI`文件夹中
打开OC编辑器将其拖入ACPI中
保存OCconfig文件
### 笔记本风扇无法转动
**原因**
`SMCSuperIO.kext`驱动未加载
**解决**
将缺少的驱动复制到`\EFI\OC\Kexts`文件夹中
打开OC编辑器将其拖入Kernel中
调整`.kext`顺序
保存OCconfig文件
> linux下`.kext`文件可能是一个文件夹，请将其当作文件看待
> 关于`.kext`的顺序请参照[Kexts 微调 - 国光的黑苹果安装教程：手把手教你配置 OpenCore](https://apple.sqlsec.com/3-%E5%87%86%E5%A4%87%E5%B7%A5%E4%BD%9C/3-8/)
### CPU温度无法读取
**原因**
`SMCProcessor.kext`驱动未加载
**解决**
同上
### typec口无法使用
**原因**
`USBInjectAll.kext`驱动未加载
> 该驱动已经过时，但仍可使用
## 参考
[国光的黑苹果安装教程](https://apple.sqlsec.com/)
[OpenCore Install Guide](https://dortania.github.io/OpenCore-Install-Guide/)
[黑苹果安装教程OC引导「建议收藏」 腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/2032334)
[stayboogy's efi](https://github.com/stayboogy/Hackintosh_Dell-Inspiron-5570_Catalina)
[Mateo1234454545‘s efi](https://github.com/Mateo1234454545/DELL-5570-Hackintosh)
[cfglock解锁教程 bilibili阿风](https://www.bilibili.com/video/BV1gb4y117FK/?spm_id_from=333.788.recommend_more_video.4)