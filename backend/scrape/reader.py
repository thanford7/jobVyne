import asyncio
import logging
from urllib.request import urlopen

import aiohttp
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)

class WebReader:
    """Read URLs"""
    MAX_CONNECTIONS = 5

    def __init__(self):
        self.conn_sem = asyncio.Semaphore(self.MAX_CONNECTIONS)
        self.session = aiohttp.ClientSession()
        self.tasks = []

    def read_sync(self, url):
        page = urlopen(url)
        html = page.read().decode('utf-8')
        return BeautifulSoup(html, 'html.parser')

    async def _read_async(self, url, cb):
        async with self.conn_sem:
            try:
                async with self.session.get(url) as resp:
                    try:
                        html = await resp.text()
                    except Exception as ex:
                        html = 'UNPARSEABLE'
                    await cb(BeautifulSoup(html, 'html.parser'))
            except:
                logger.info(f'Could not read URL {url}')

    def read_async(self, url, cb):
        """Read a URL and call cb when the data returns"""
        future = self._read_async(url, cb)
        self.tasks.append(future)

    def complete(self):
        future = asyncio.gather(*self.tasks)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
        asyncio.run(self.session.close())

