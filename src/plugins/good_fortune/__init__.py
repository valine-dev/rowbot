'''运势:
    只要是在oneshot群里的bot就一定会有的今日运势功能。
    这里的实现实际上是把请求人的ID、日期和时间塞到一个dict里面，
    揉成str，取hash，再丢到随机数的seed里面
    这样保证了同一个人每天对一个事件的运势是不变的
    之前我还想着用数据库呢（笑）但很可惜异步DB是个麻烦活
    哦对，还有隐藏的特殊运势
    1./运势 [事件]
        事件可以不存在，那么测出来的想必就是今日总体运势

'''
import hashlib
import random
from datetime import datetime
from os.path import join

import httpx
import nonebot
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.log import logger
from nonebot.typing import T_State

from .config import Config

# 从全局配置读取配置
global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

proxies: dict = {
        "http://": plugin_config.proxy_http_url,
        "https://": plugin_config.proxy_https_url
    }

# 引入处理的事件
wish = on_command('运势', priority=5)

# 所有可能出现的签语 这里的{e}会被请求的事件替换，{kotoba}会被签语替代, {uid}会被目标用户ID取代
# 您应当在result文件下编辑，其中 *** 行将隔开普通结果与特殊结果， /// 行隔开每个结果
results: list = []

# 特殊签语
special_results: list = []

# 载入签语
with open(join(__path__[0], 'results'), 'r', encoding='UTF-8') as file:
    raw = file.read()
chunks = raw.split('***')

results = chunks[0].split(r'///')
special_results = chunks[1].split(r'///')


@wish.handle()
async def wish_handler(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    dice = random.SystemRandom().randint(0, 100)

    array = []

    if dice <= plugin_config.special:
        array = special_results
    else:
        array = results

    e = args if args else '今日'
    now = datetime.now().strftime(r'%Y/%m/%d')
    usr = event.get_user_id()

    result = await make_wish(
            {
                'usr': usr,
                'date': now,
                'event': e
            },
            array,
            plugin_config.use_hitokoto
        )
    await wish.finish(result)


async def make_wish(
    event: dict,
    choices: list,
    hitokoto: bool
):
    '''生成签文的逻辑

    Args:
        event (dict): 要求签的事件（一般包含用户、时间、事件三个字段）
        choices (list): 可以选择的签文
        hitokoto (bool): 是否要加入一句箴言
    '''

    seed = hashlib.blake2s(
        str(event).encode('utf-8')
    ).hexdigest()
    logger.debug(f'Wish Requested with {event}.')
    random.seed(seed)
    result = random.choice(choices)
    kotoba = ''
    if hitokoto:
        async with httpx.AsyncClient(proxies=proxies) as client:
            response = await client.get(
                'https://v1.hitokoto.cn?c=k',  # 哲学分类
            )
        if not response.is_error:
            r = response.json()
            kotoba = f'{r["hitokoto"]} —— {r["from_who"]} 「{r["from"]}」'

    return result.format(
        e=event['event'],
        kotoba=kotoba,
        uid=event['usr']
    )[1:]
