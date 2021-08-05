from os import path

import nonebot
from nonebot import on_command, require
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.typing import T_State

from . import __path__
from .config import Config
from .twitter import fetch

# 从全局配置读取配置
global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

# 引入处理的事件
recent = on_command('今日新图', rule=to_me(), priority=5)
trend = on_command('今日热图', rule=to_me(), priority=5)
tracker = require('nonebot_plugin_apscheduler').scheduler

# 在cache机制搭起来之前先用全局变量解决持久化问题
__cache__ = {'last_track_id': {}}

for member in plugin_config.retweet_control_users:
    # 初始化 cache
    __cache__['last_track_id'][member] = ''


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


@tracker.scheduled_job("cron", hour="*/1", id="feed")
async def fetch_():
    '定时追踪指定用户最新信息并推送'
    bot = nonebot.get_bots().items()[0][1]  # 用第一个BOT
    cpth = path.join(__path__, 'cache')
    for member in plugin_config.retweet_control_users:
        tweet = await fetch(
            plugin_config.bearer_token,
            member,
            'recent',
            plugin_config.proxies,
            '1'
        )[0]
        if tweet.status_id != __cache__['last_track_id'][member]:
            __cache__['last_track_id'][member] = tweet.status_id
            content = f'''用户@{member}有了新动态：
            {tweet.text}

            '''
            for cache in tweet.media_local_cache:
                content += f'[CQ:image,file={cpth + cache}]\n'
            bot.send(content)


async def pic_fetch_common(tpe: str, tag: str):
    '今日热图和今日新图是一回事'

    if not tag.startswith('#'):
        tag = '#' + tag

    tweets = await fetch(
        plugin_config.bearer_token,
        tag,
        tpe,
        plugin_config.proxies,
        '3'
    )

    cpth = path.join(__path__, 'cache')
    result = ''
    for tweet in tweets:
        seg = f'作者: @{tweet.author_id}'
        for cache in tweet.media_local_cache:
            seg += f'[CQ:image,file={cpth + cache}]'
        seg += '\n'
        result += seg
    return result
