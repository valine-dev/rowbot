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
from nonebot.log import logger

from .config import Config
from .platforms._model import Work

# 从全局配置读取配置
global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

# 将 Platform 读取为子插件
_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / 'platforms').resolve()))

# 按需取用
platforms = {}
for p in plugin_config.retweet_platforms:
    platforms[p] = require(p)

logger.debug(f'Loaded platforms with {platforms}')

# 设置代理
proxies: dict = {
        'http://': plugin_config.proxy_http_url,
        'https://': plugin_config.proxy_https_url
    }

# 定义处理的事件
recent = on_command('今日新图', priority=1)
tracker = require('nonebot_plugin_apscheduler').scheduler


async def selector(
    target: str,
    amount: int,
    since: datetime,
    only_media: bool = True
) -> list[Work]:
    '''根据目标内容确定使用哪个platform的fetch

    Args:
        target (str): 查询的内容，例如 #hashtag, @user, u/user, r/subreddit 等
        amount (int): 返回多少个结果
        only_media (bool): 是否只返回有媒体的结果

    Returns:
        list[Work]: 返回的work列表
    '''
    pfetch: callable = None
    for platform, exports in platforms.items():
        for prefix in exports['prefixes']:
            if target.startswith(prefix):
                pfetch = exports['fetch']
                logger.debug(
                    f'Retweet v3: Of target {target} found platform {platform}'
                )
                break
    if pfetch is None:
        logger.warning(f'Of target {target}, no platform found.')
        return None
    return await pfetch(
        target,
        since,
        amount,
        only_media,
        proxies
    )


@recent.handle()
async def recent_handler(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    tag = args if args else plugin_config.retweet_default

    bot.send(event, f'正在获取今日{tag}的最新图')

    result = await selector(tag, 3, datetime.today())
    if result is None:
        recent.reject(f'未找到与{tag}匹配的平台，或许是还没支持。')
    for work in result:
        pics = ''.join([x for x in work.media.get_segment()])
        wording = f'由{work.author}绘制\n{work.text}\n{pics}\n{work.url}'
        await recent.send(wording)
    recent.finish('以上です！')


# 建立 cache
__cache__ = {'latest_date': {}}
for entity in plugin_config.retweet_control:
    # 初始化 cache
    __cache__['latest_date'][entity] = ''


@tracker.scheduled_job('cron', hour='*/1', id='feed')
async def feed():
    bots = nonebot.get_bots()
    for entity in plugin_config.retweet_control:

        prev = __cache__['latest_date'][entity]
        latest: list[Work] = await selector(entity, 1, prev, False)

        if latest is None:
            return

        amount = len(latest)

        if amount == 0:
            return None

        __cache__['latest_date'][entity] = latest[0].date

        for identity, bot in bots.items():
            for group in plugin_config.retweet_feeds:
                await bot.send_group_msg(
                    group_id=group,
                    message=f'{entity}过去的一小时里多了{amount}新条消息！'
                )

                for msg in latest:
                    pics = ''
                    for media in msg.media:
                        pics += media.get_segment()
                    final = f'{msg.author}:\n{msg.text}' + pics
                    await bot.send_group_msg(
                        group_id=group,
                        message=final
                    )

                logger.debug(
                    f'Retweet v3: Bot {identity} fed {group}'
                )
