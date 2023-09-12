import asyncio
import logging
from urllib import request

import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class WebReader:
    """Read URLs"""
    MAX_CONNECTIONS = 5
    
    def __init__(self):
        self.conn_sem = asyncio.Semaphore(self.MAX_CONNECTIONS)
        self.session = aiohttp.ClientSession(headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        self.tasks = []
    
    def read_sync(self, url):
        req = request.Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        page = request.urlopen(req)
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
                logger.info(f'Error reading or summarizing URL {url}')
    
    def read_async(self, url, cb):
        """Read a URL and call cb when the data returns"""
        future = self._read_async(url, cb)
        self.tasks.append(future)
    
    def complete(self):
        future = asyncio.gather(*self.tasks)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
        asyncio.run(self.session.close())
