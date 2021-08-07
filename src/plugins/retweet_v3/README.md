# Retweet v3
> ### 赤い赤い 赤い仮面のV3

意识到之前的 Retweet 写得实在稀烂，决定重构一个新版本出来，这个版本实现了不少旧版难以实现的特性（例如更加简单的多平台支持）也丢掉了很多因为刚开始写对cqhttp和nonebot不熟悉的地方，甚至默认的`twitter_api.py`也使用了最新的接口，总之BIGGER(实际上框架更简洁了) & BETTER.

## 原理
在这里简单阐述下v3的工作方式。

首先，v3中有三个重要的概念： platform 、 Work 类 和 selector 。它们构成了一个这样的工作流：在 matcher 接收到必要的参数之后，将会调用 selector ，此时 selector 将根据请求的前缀寻找合适的 platform ，并调用 platform 相应的 fetch() 函数，最后把数据打包成 Work 实例返回给 matcher ，完成一次请求。

其中 platfrom 是一个标准的 nonebot2 插件，位于 retweetv3/platforms ，并必须有两个 export 项： 变量 `prefixes: list` 和函数 `fetch()` 其中 prefixes 是一个字符串列表，意味着这个 platform 接受什么样的前缀 （若重复将询问enduser指定平台），而 `fetch()` 的声明如下：

```python
# 请注意，您应当 **保持参数名不变**
async def fetch(
    target: str,  # 要获取的对象，根据平台不同可以为 #hashtag, @user, u/user, r/subreddit 等...
    since: datetime,  # python的标准datetime对象 指明了最远查询的日期
    max_amount: int,  # 指明本次最多返回多少个对象（最好是在请求时实现）
    only_media: bool = True,  # 是否只返回带有媒体（图像、视频）的结果
    proxy: dict = {},  # 请求时所用的代理，格式取决于您使用的网络库
) -> list[Work]:  # 返回值是Work类实例组成的列表
    pass

# 对具体api的请求在platform中完成，因此需要将代理信息传入
# 默认使用httpx，统一传入的代理格式如下
# 当然您也可以忽视传入的proxy，从插件config里调一个，以便使用自己熟悉的库
# 但请使用异步网络库
proxy: dict = {
    'http://': 'http://127.0.0.1:8080/',
    'https://': 'http://127.0.0.1:8080/'
}
```
如果您的插件实现了 `fetch()` 并声明了 `prefixes` 并使用nonebot2的export机制开放，那么这个插件就是一个合法的 platform

