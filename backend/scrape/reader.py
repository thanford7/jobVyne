import asyncio
import logging
import sqlite3
from urllib.request import urlopen

import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class DocCache:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(f'media/{db_name}.sqlite3')
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists cache (key, val);')

    def clear(self):
        self.cursor.execute('delete from cache;')

    def get(self, key):
        self.cursor.execute('select key, val from cache where key = ?;', (key,))
        all_rows = self.cursor.fetchall()
        if len(all_rows) == 1:
            return all_rows[0][1]
        return None

    def put(self, key, val):
        self.cursor.execute('insert into cache (key, val) values (?, ?)', (key, val))
        self.conn.commit()

class WebReader:
    """Read URLs"""
    MAX_CONNECTIONS = 5

    def __init__(self):
        self.conn_sem = asyncio.Semaphore(self.MAX_CONNECTIONS)
        self.session = aiohttp.ClientSession()
        self.cache = DocCache('web_reader_cache')
        self.tasks = []

    def read_sync(self, url):
        if not (html := self.cache.get(url)):
            page = urlopen(url)
            html = page.read().decode('utf-8')
            self.cache.put(url, html)
        return BeautifulSoup(html, 'html.parser')

    async def _read_async(self, url, cb):
        if html := self.cache.get(url):
            cb(BeautifulSoup(html, 'html.parser'))
        else:
            async with self.conn_sem:
                async with self.session.get(url) as resp:
                    try:
                        html = await resp.text()
                    except Exception as ex:
                        html = 'UNPARSEABLE'
                    self.cache.put(url, html)
                    cb(BeautifulSoup(html, 'html.parser'))

    def read_async(self, url, cb):
        """Read a URL and call cb when the data returns"""
        future = self._read_async(url, cb)
        self.tasks.append(future)

    def complete(self):
        future = asyncio.gather(*self.tasks)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
        asyncio.run(self.session.close())

