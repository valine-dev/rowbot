import os.path

import httpx
from nonebot.log import logger


class Tweet:
    def __init__(
        self,
        status_id: str,
        author_id: str,
        author_name: str,
        date: str,
        text: str,
        media_url: list
    ):
        self.status_id = status_id
        self.author_id = author_id
        self.author_name = author_name
        self.date = date
        self.text = text
        self.media_url = media_url

        self.media_local_cache = []

    async def cache_all(self, proxies: dict):
        for i in range(0, len(self.media_url)):
            fn = f'{self.status_id}_{self.author_name}_p{i}'
            await self._cache(self.media_url[i], fn, proxies)

    async def _cache(self, url: str, target: str, proxies: dict):
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
                    logger.debug(
                        f'Downloading {target} with {int(now / total * 100)} %'
                    )

        self.media_local_cache.append(target)
        logger.debug(f'Cache {target} download complete')
