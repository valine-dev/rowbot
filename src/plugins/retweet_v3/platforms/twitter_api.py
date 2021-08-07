'''Twitter-API Platform
一个默认的Platform，用于通过API与Twitter沟通
'''

from datetime import datetime

import nonebot
import httpx
from nonebot.plugin import export
from pydantic import BaseSettings

from .model import Work, Media

export = export()
prefixes = ['@', '#']
export.prefixes = prefixes


# 定义一个配置类
class Config(BaseSettings):
    twitter_api_token: str = ''

    class Config:
        extra = "ignore"


# 从全局配置读取配置
global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())


async def _get(
    endpoint: str,
    query: str,
    api_version: str = '2',
    attach_header: dict = {},
    proxy: dict = {}
) -> dict:
    url = f'https://api.twitter.com/{api_version}/{endpoint}'
    token = plugin_config.twitter_api_token

    headers: dict = {
        **{'Authorization': f'Bearer {token}'}, **attach_header
    }

    proxies = proxy if proxy != {} else None

    async with httpx.AsyncClient(proxies=proxies) as client:
        response = await client.get(
            url,
            headers=headers,
            params=query
        )

    if response.is_error:
        return None

    return response.json()


@export
async def fetch(
    target: str,
    since: datetime,
    max_amount: int,
    only_media: bool = True,
    proxy: dict = {},
) -> list[Work]:

    has_media = ' has:media' if only_media else ''
    keyword = target if target.startswith('#') else f'from:{target[1:]}'

    raw = await _get(
        'tweets/search/recent',
        {
            'query': f'{keyword} -is:retweet{has_media}',
            'end_time': since.strptime(r'%Y-%m-%dT00:00:00.000Z'),
            'media.fields': 'type,url',
            'user.fields': 'name,username',
            'tweet.fields': 'created_at',
            'max_results': max_amount
        },
        proxy=proxy
    )
    result = []
    for tweet in raw["data"]:
        uid = tweet['id']
        usrn = tweet['includes']['users'][0]['username']
        o = Work(
            uid,
            usrn,
            tweet['includes']['users'][0]['name'],
            datetime.strptime(tweet['create_at'], r'%Y-%m-%dT%H:%M:%S.000Z'),
            f'https://twitter.com/{usrn}/status/{uid}',
        )
        for media in tweet['includes']['media']:
            o.add_media(
                Media(
                    media['type'],
                    media['url']
                )
            )
        result.append(o)
    return result
