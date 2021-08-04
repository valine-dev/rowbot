import asyncio
import os.path

import httpx
from nonebot.log import logger

# wrapper for twitter api interactions


class Tweet:
    def __init__(self, status_id: str, author_id: str, author_name: str, date: str, media_url: list): 
        self.status_id = status_id
        self.author_id = author_id
        self.author_name = author_name
        self.date = date
        self.media_url = media_url

        self.media_local_cache = []

    async def cache_all(self, proxies: dict):
        for i in range(0, len(self.media_url)):
            fn = f'{self.status_id}_{self.author_name}_p{i}'
            await self.cache(self.media_url[i], fn, proxies)

    async def cache(self, url: str, target: str, proxies: dict):
        '''download certain resource to cache.

        Args:
            url (str): the source
            url (str): the name
            proxies (dict): HTTP only
        '''

        logger.debug(f'Cache {target}_ download begins, from {url}')
        client = httpx.AsyncClient(proxies=proxies)
        file_path = os.path.abspath(f'{__path__}/cache/{target}')

        # Skip when file exsists
        if os.path.exists(file_path):
            self.media_local_cache.append(target)
            logger.debug(f'Cache {target} already exsists')
            return

        with open(file_path, 'xb') as f:

            async with client.stream('GET', url) as response:

                total = int(response.headers['Content-Length'])

                async for chunk in response.aiter_bytes():
                    f.write(chunk)

                    now = response.num_bytes_downloaded
                    logger.debug(f'Downloading {target} with {int(now / total * 100)} %')

        self.media_local_cache.append(target)
        logger.debug(f'Cache {target} download complete')


async def request_construct(
    bearer_token: str,
    endpoint: str,
    query: dict,
    method: str='GET',
    api_version: str='1.1',
    appendix_header: dict={},
    proxies: dict={}
) -> httpx.Response:
    '''Function that construct a query request while returning a response.

    Args:
        bearer_token (str): bearer_token on behalf of the application
        endpoint (str): endpoint, or resource like 'tweets/search/recent' or 'search/tweets.json'
        query (str): query dict like:
            {
                'q': 'imn',
                'result_type': 'popular',
            }
        method (str): 'GET' or 'POST'
        api_version (str, optional): The API version. Defaults to '1.1'.
        appendix_header (dict, optional): only if you need more header info, 
            reminds that you may replace the whole auth section. Defaults to empty.
        proxies (dict, optional): HTTP only. For example:
            {
                'http://': 'http://localhost:8030',
                'https://': 'http://localhost:8031',
            }

    Returns:
        httpx.Response: Standard Response object of httpx
    '''

    # make query string
    q = '&'.join([f'{x[0]}={x[1]}' for x in query.items()])

    # construct request
    url: str = f'https://api.twitter.com/{api_version}/{endpoint}?{q}'
    headers: dict = {**{'Authorization': f'Bearer {bearer_token}'}, **appendix_header}

    # send and get response
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, headers=headers)
    return response


async def fetch(
    bearer_token: str,
    obj: str,
    order: str,
    amount: int
) -> list:
    '''fetch

    Args:
        bearer_token (str): bearer_token on behalf of the application
        obj (str): the exact thing you want to fetch from (starts with a '@' means it's a person, with a '#' means it's a hashtag)
        order (str): the order in list that returns, can be 'recent' or 'popular'

    Returns:
        list: list contains all the tweets packed in object form
    '''

    response: httpx.Response = request_construct(
        bearer_token,
        'tweets/search/recent',
        {
            'query': obj,
            'result_type': order,
            'count': amount,
            'include_entities': 'true'
        },
    )

    if response.is_error:
        logger.error(f'ERROR OCCURRED WHEN REQUESTING {response.url} WITH CODE {response.status_code}')
        return None

    # aquire payload
    content = response.json()

    # pack tweets
    result = []
    for raw_tweets in content['statuses']:
        o = Tweet(
            raw_tweets['id_str'],
            raw_tweets['user']['id_str'],
            raw_tweets['user']['name'],
            raw_tweets['created_at'],
            [x['media_url'] for x in raw_tweets['extended_entities']['media']]
        )
        result.append(o)

    return result
