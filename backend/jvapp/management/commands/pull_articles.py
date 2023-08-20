import abc
import logging
from collections import deque

import trafilatura
from django.core.management import BaseCommand

from jvapp.models.content import Article
from jvapp.utils import ai
from scrape.reader import WebReader

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Pull articles from aggregation websites'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit the number of articles to pull',
        )

    def handle(self, *args, **options):
        limit = options['limit']
        num_articles_pulled = 0

        web_reader = WebReader()
        articles = []
        try:
            for article_source_class in article_source_classes:
                # FIXME: Will unnecessarily instantiate classes after limit is hit
                article_source = article_source_class(web_reader, articles)
                while article_source.has_more() and num_articles_pulled < limit:
                    article_source.get_next()
                    num_articles_pulled += 1
        finally:
            # TODO: Make this a 'with' structure
            web_reader.complete()

        for article in articles:
            article.save()


class ArticleSource(abc.ABC):
    def __init__(self, web_reader:WebReader, articles:list):
        self.web_reader = web_reader
        self.articles = articles

    async def get_article(self, url, title, bs):
        SUMMARIZE_PROMPT = (
            'You are summarizing an article in 3-5 sentences. Your response should be RFC8259 compliant JSON in the format: '
            '{"summary": "(summary of article)"}'
        )
        text = trafilatura.extract(str(bs))

        logger.info(f'Calling AI for summary of {url}')
        resp, _ = await ai.ask([
            {'role': 'system', 'content': SUMMARIZE_PROMPT},
            {'role': 'user', 'content': text[:1000]}  # TODO: Can we chunk article text into multiple requests?
        ], is_test=False)

        self.articles.append(Article(
            url=url,
            title=title,
            summary=resp.get('summary'),
            companies=[],
        ))

    @abc.abstractmethod
    def has_more(self):
        raise NotImplemented()

    @abc.abstractmethod
    def get_next(self):
        raise NotImplemented()


class ListArticleSource(ArticleSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = deque()

    def get_next(self):
        url, title = self.queue.popleft()
        async def cb(article_bs):
            await self.get_article(url, title, article_bs)
        return self.web_reader.read_async(url, cb)

    def has_more(self):
        return len(self.queue) > 0


class HN(ListArticleSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        index_page_bs = self.web_reader.read_sync('https://news.ycombinator.com/')

        # Only look at articles on the first page
        for athing_bs in index_page_bs.find_all('tr', class_='athing'):
            # Skip articles that we've already captured
            a_bs = athing_bs.find('span', class_='titleline').find('a')
            url = a_bs.get('href')
            if Article.objects.filter(url=url).exists():
                continue
            title = a_bs.text
            self.queue.append((url, title))

article_source_classes = [HN]