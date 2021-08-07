'''Retweet:
    Retweet总共包含两个功能
    1./今日新图 [标签]
        该功能负责查询特定标签下今日最新的推文
    2.自动推送
        该功能会自动推送在配置里指定的用户/标签的最新消息
'''
from pathlib import Path
from datetime import datetime

import nonebot
from nonebot import on_command, require
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State

from .config import Config
from .platforms._model import Work

# 从全局配置读取配置
global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

# 将 Platform 读取为子插件
_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "platforms").resolve()))

# 按需取用
platforms = {}
for p in plugin_config.platforms:
    platforms[p] = require(p)

# 设置代理
proxies: dict = {
        "http://": plugin_config.proxy_http_url,
        "https://": plugin_config.proxy_https_url
    }

# 定义处理的事件
recent = on_command('今日新图', priority=1)
tracker = require('nonebot_plugin_apscheduler').scheduler


async def selector(
    target: str,
    amount: int,
    only_media: bool = True
) -> list[Work]:
    """根据目标内容确定使用哪个platform的fetch

    Args:
        target (str): 查询的内容，例如 #hashtag, @user, u/user, r/subreddit 等
        amount (int): 返回多少个结果
        only_media (bool): 是否只返回有媒体的结果

    Returns:
        list[Work]: 返回的work列表
    """
    pfetch: callable
    for platform, exports in platforms:
        for prefix in exports.prefixes:
            if target.startswith(prefix):
                pfetch = exports.fetch
                break
    return await pfetch(
        target,
        datetime.today(),
        amount,
        only_media,
        proxies
    )


@recent.handle()
async def recent_handler(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    tag = args if args else plugin_config.retweet_default_tag

    bot.send(event, f'正在获取今日{tag}的最新图')

    result = await selector(tag, 3)
    for work in result:
        pics = ''.join([x for x in work.media.get_segment()])
        wording = f'由{work.author}绘制\n{work.text}\n{pics}\n{work.url}'
        await recent.send(wording)


# 在cache机制搭起来之前先用全局变量解决持久化问题
__cache__ = {'latest_id': {}}
for entity in plugin_config.retweet_control:
    # 初始化 cache
    __cache__['latest_id'][entity] = ''


@tracker.scheduled_job('cron', hour='*/1', id='feed')
async def feed():
    bots = nonebot.get_bots()
    for entity in plugin_config.retweet_control:

        # 检查更新
        latest = selector(entity, 1, False)[0]
        if latest.uid != __cache__['latest_id'][entity]:

            __cache__['latest_id'][entity] = latest.uid
            pics = ''.join([x for x in latest.media.get_segment()])
            wording = f'{entity}有了一条新消息\n{latest.text}\n{pics}'

            for identity, bot in bots:
                for group in plugin_config.retweet_feeds:
                    await bot.send_group_msg(
                        group_id=group,
                        message=wording
                    )
