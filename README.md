<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="./logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# Rowbot
</div>

一个大概可能会被用于 OneShot 相关QQ群（不已经一堆BOT了吗啊喂）的群聊机器人核心，基于[NoneBot2](https://v2.nonebot.dev/)框架（并默认使用 CQHTTP 协议）。由 Red_Cell 荣誉粗制滥造。

> 温馨提示，本repo包含但不限于以下要素：
> 
> - 令人感到不适程度的 python 水平
> - 该写 docstring 的地方不写，没人看的 private 函数巴不得从盘古开天辟地写
> - 除了 Red_Cell 以外没人知道的工作方式
> - 鸽子以螺旋桨的形式起飞
> - PEP8 建议我把 repo 删了
> - 一点也不正经的注释
> - 写 README 比写代码有意思多了
> - # ~~*风控WRNM*~~


## 如何使用
> *RTFM！*
>
> *？我Manual呢*
>
> *哦，没有Manual啊，那没事了。*

将本repo下载或git clone到本地，编写配置文件(.env.*)，并安装任意CQHTTP协议端，按照[这里](https://v2.nonebot.dev/guide/cqhttp-guide.html)的指南连接本核心与协议端，您就可以使用了
### 那怎么配置呢？
阅读根目录下的 `.env.example` ，里面对每个项目都打了注释，但您应该复制一份，并创建 `.env.dev` 和 `.env.prod` 对应开发环境和生产环境的配置
### WDNMD我看不懂
Read-The-Fine-Manual（指[nonebot2文档](https://v2.nonebot.dev/)）

当然，之后有时间**可能会做一个指南**的**咕**

## 功wa能keng
> *（BOT）：我现在tm什么都不会呢，到时候考出来也就个40多分。*

### RetweetV3（COMPLETE but UNTESTED）
Rowbot核心功能，追踪Twitter的特定用户或tag，定时推送或手动调出最新的内容

> *现已重构推出V3版，可自行拓展其他平台，请在 [这里](./src/plugins/retweet_v3/README.md) RTFM*

获取Twitter数据依赖于官方API，~~但由于开发者还没拿到API权限，所以能不能用开发者也不知道~~

~~干脆用爬虫得了~~

### 运势（AVALIABLE）
**传统艺能**

每人每天每个事件只有唯一解的加强版运势

现已加入 ***Hitokoto*** 强力支持

### 30-30 Repeater（AVALIABLE）
人类的本质是复读机

### NikoMaker（PENDING）
定做Niko对话框

## 还想要更多？
> *~~没办法，你还真是难以满足呢w~~*

您可以发发issue、DM轰炸提提建议或者干脆发个PR

## 开源协议
本项目使用[WTFPLv2许可证](http://www.wtfpl.net/)，这意味着对于本项目，字面意义上，您他妈的爱咋咋地，更多详情请查看 LICENSE 文件。并且本项目作为自由软件，概无保修。