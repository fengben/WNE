# WNE
WNE Not Evernote

#Why
*  作为印象笔记的重度用户（截止到今天，笔记5301条），我已经受够了，粉转路人。原因有：
  *  原生不支持markdown
  *  担心这只曾经的独角兽快挂掉而提心吊胆
  *  愚蠢的字符转义功能，尤其是`-`、`"`、`'`。一旦粘贴代码，非常蛋疼
  
说了这么多，似乎太绝情，毕竟曾经爱过呀。

即便现在自己构建笔记系统，印象笔记的优秀特性依然是灵感来源

#架构
*  采用markdown+jupyter+git构建自己的笔记本
  *  笔记保存为markdown文件
  *  使用jupyter来写作
  *  使用git管理笔记

###一般notebook的常用特性
列举一般笔记系统的常用特性

*  元信息(metadata)
  *  title
  *  tag
  *  时间戳
  *  notebook name
*  搜索功能
  *   针对元信息的搜索，诸如标题搜索/标签搜索
  *   在范围内搜索，诸如：
    *   最近笔记
    *   按笔记本或tag搜索
  *  组合逻辑

###实现
*  针对元信息
  *  title可以文件名实现，或者在文本里标识，正则提取，类似pelican
  *  tag也模仿pelican
  *  时间戳，文件系统天然带有
  *  使用文件夹实现notebook name
*  针对搜索功能
  *  unix/linux工具链：ack/grep
  *  elasticsearch
  *  github/gitlab本身支持仓库内搜索
  *  打造搜索脚本在client里用/在jupyter中开一个terminal，结合ack/grep和percol

###Maybe
由于围绕纯文本，十分轻量化，拓展起来十分便利

*  C/S架构
 *  server对外提供REST接口
 *  client包括
    *  类似geeknote的命令行工具
    *  微信作为客户端

#YAN可能吸引你的地方
*  文本化，你可以对接到任何你喜欢的unix/linux工具套件（vim/sed/ack/grep/），这个特性对技术人员十分有利
  *  支持正则
*  版本管理
  *  分布式的鸡蛋：你不依赖任何平台，如果你愿意可以放到github/gitlab/gogs/...上
*  你花在阅读代码上的时间远超过写它，对于笔记应该也是。利用unix/linux工具链，你可以以任何细粒度搜索笔记
*  你的笔记，如果你不愿意分享，它本该只对你可见，所以，你为何要把它交给别人
*  All in one，你的所有东西都可以采用markdown书写，之后采用markdown生态链把它装化为任何东西（诸如ppt，docx，html）
*  直接用作博客
