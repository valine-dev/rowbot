import httpx
from nonebot.log import logger

from .model import Tweet

# wrapper for twitter api interactions
# 这里为了能让 Twitter 审核看懂用英文注释


async def _request_construct(
    bearer_token: str,
    endpoint: str,
    query: dict,
    method: str = 'GET',
    api_version: str = '1.1',
    appendix_header: dict = {},
    proxies: dict = {}
) -> httpx.Response:
    '''Function that construct a query request while returning a response.

    Args:
        bearer_token (str): bearer_token on behalf of the application
        endpoint (str): endpoint, or resource like 'tweets/search/recent'
            or 'search/tweets.json'
        query (str): query dict like:
            {
                'q': 'inm',
                'result_type': 'popular',
            }
        method (str): 'GET' or 'POST'
        api_version (str, optional): The API version. Defaults to '1.1'.
        appendix_header (dict, optional): only if you need more header info,
            reminds that you may replace the whole auth section.
            Defaults to empty.
        proxies (dict, optional): HTTP only. For example:
            {
                'http://': 'http://localhost:8030',
                'https://': 'http://localhost:8031',
            }

    Returns:
        httpx.Response: Standard Response object of httpx
    '''

    # make query string

    # construct request
    url: str = f'https://api.twitter.com/{api_version}/{endpoint}'
    headers: dict = {
        **{'Authorization': f'Bearer {bearer_token}'}, **appendix_header}

    # send and get response
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            url,
            headers=headers,
            params=query
        )
    return response


async def fetch(
    bearer_token: str,
    obj: str,
    order: str,
    proxies: dict,
    amount: int
) -> list:
    '''fetch tweets

    Args:
        bearer_token (str): bearer_token on behalf of the application
        obj (str): the exact thing you want to fetch from
            (starts with a '#' means it's a hashtag)
        order (str): the order in list that returns,
            can be 'recent' or 'popular' (don't fit for person)

    Returns:
        list: list contains all the tweets packed in object form
    '''

    response: httpx.Response = _request_construct(
        bearer_token,
        'search/tweets.json',
        {
            'q': obj,
            'result_type': order,
            'count': amount,
            'include_entities': 'true'
        },
        proxies=proxies
    ) if obj.startswith('#') else _request_construct(
        bearer_token,
        'proxiesstatuses/user_timeline.json',
        {
            'screen_name': obj,
            'count': amount,
            'exclude_replies': 'true',
            'include_rts': 'false'
        },
        proxies=proxies
    )

    if response.is_error:
        logger.error(
            f'ERROR OCCURRED WHEN REQUESTING {response.url}\
                WITH CODE {response.status_code}')
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
            raw_tweets['text'],
            [x['media_url'] for x in raw_tweets['extended_entities']['media']]
        )
        result.append(o)

    return result
