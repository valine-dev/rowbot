'''Retweet:
    Retweet总共包含三个功能
    1./今日热图/新图 [标签]
        该功能负责查询特定标签最新/最热的推文，返回三个
    2./自动推送
        该功能会自动推送在配置里指定的用户/标签的最新消息
'''
import nonebot
from nonebot import on_command, require
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import MessageSegment

from .config import Config
from .twitter import fetch

# 从全局配置读取配置
global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

proxies: dict = {
        "http://": plugin_config.proxy_http_url,
        "https://": plugin_config.proxy_https_url
    }

# 引入处理的事件
recent = on_command('今日新图', priority=1)
trend = on_command('今日热图', priority=1)


@recent.handle()
async def recent_handler(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    tag = args if args else plugin_config.retweet_default_tag
    await recent.finish(pic_fetch_common('recent', tag))


@trend.handle()
async def trend_handler(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    tag = args if args else plugin_config.retweet_default_tag
    await recent.finish(pic_fetch_common('popular', tag))


# 在cache机制搭起来之前先用全局变量解决持久化问题
__cache__ = {'last_track_id': {}}
for member in plugin_config.retweet_control_users:
    # 初始化 cache
    __cache__['last_track_id'][member] = ''


async def fetch_():
    '定时追踪指定用户/标签最新信息并推送'
    bot = nonebot.get_bots()[plugin_config.self_identity]

    for member in plugin_config.retweet_control_users:
        tweet = await fetch(
            plugin_config.bearer_token,
            member,
            'recent',
            proxies,
            '1'
        )[0]
        if tweet.status_id != __cache__['last_track_id'][member]:
            __cache__['last_track_id'][member] = tweet.status_id
            content = f'''用户@{member}有了新动态：
            {tweet.text}

            '''
            for url in tweet.media_url:
                content += MessageSegment.image(url)
            bot.send(content)


async def pic_fetch_common(tpe: str, tag: str):
    '今日热图和今日新图是一回事，这里不该拆成俩Matcher的，但我希腊奶'

    if not tag.startswith('#'):
        tag = '#' + tag

    tweets = await fetch(
        plugin_config.bearer_token,
        tag,
        tpe,
        proxies,
        '3'
    )

    result = ''
    for tweet in tweets:
        seg = f'作者: @{tweet.author_id}'
        for url in tweet.media_url:
            seg += MessageSegment.image(url)
        seg += '\n'
        result += seg
    return result
