import abc
import logging
from collections import deque

import trafilatura

from jvapp.models.content import Article
from jvapp.models.employer import Taxonomy
from jvapp.utils import ai
from scrape.reader import WebReader

logger = logging.getLogger(__name__)

# 100 tokens = ~75 words (https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)
# 4k tokens = ~3000 words
# 16k tokens = ~12000 words
# Considering the response to be a certain number of "words", use that to figure out the
# text cutoff lengths of articles.
RESP_WORDS = 500
M4K_WORDS = 3000
M4K_CUTOFF_WORDS = M4K_WORDS - RESP_WORDS
M16K_WORDS = 12000
M16K_CUTOFF_WORDS = M16K_WORDS - RESP_WORDS
INDUSTRIES, PROFESSIONS = (
    [t.name for t in Taxonomy.objects.filter(tax_type=tt)]
    for tt in (Taxonomy.TAX_TYPE_INDUSTRY, Taxonomy.TAX_TYPE_PROFESSION)
)
SUMMARIZE_PROMPT = (
    'You are summarizing an article in 3-5 sentences. Use the author\'s point of view and tone of voice when summarizing. '
    'Also, capture the names and URLs of any companies mentioned, any industries the article involves, and any professions the article involves. \n'
    f'The allowed industries are: {", ".join(INDUSTRIES)}\n'
    f'The allowed professions are: {", ".join(PROFESSIONS)}\n'
    'Do not include any explanations, only provide a RFC8259 compliant JSON response following this format without deviation.:\n'
    '{'
        '"summary": (summary of article),'
        '"companies": [{"company_name": company, "company_url": URL of the company if available}, ...],'
        '"industries": [(list of industries)]'
        '"professions": [(list of professions)]'
    '}'
)

def pull_articles(limit):
    num_articles_pulled = 0

    web_reader = WebReader()
    articles = []
    try:
        for article_source_class in article_source_classes:
            article_source = article_source_class(web_reader, articles)
            while article_source.has_more() and num_articles_pulled < limit:
                article_source.get_next()
                num_articles_pulled += 1
    finally:
        # TODO: Make this a 'with' structure
        web_reader.complete()

    for article in articles:
        article.save()
        tax_list = getattr(article, 'tax_list', [])
        for prop_name, tax_type, name in tax_list:
            try:
                taxonomy = Taxonomy.objects.get(tax_type=tax_type, name=name)
            except Taxonomy.DoesNotExist:
                logger.info(f'AI chose invalid {tax_type} taxonomy {name} for URL {article.url}')
                continue
            m2m = getattr(article, prop_name)
            m2m.add(taxonomy)
        article.save()

class ArticleSource(abc.ABC):
    source = None

    def __init__(self, web_reader:WebReader, articles:list):
        self.web_reader = web_reader
        self.articles = articles

    async def get_article(self, url, title, bs):
        logger.info(f'Calling for batched summary of {url}')

        text = trafilatura.extract(str(bs))
        logging.info(f'Summarizing text:\n{text}')
        words = text.split(' ')
        # Above the 4k cutoff, use 16k model; above the 16k cutoff, truncate
        model = ai.M4K
        if len(words) > M4K_CUTOFF_WORDS:
            model = ai.M16K
            words = words[:M16K_CUTOFF_WORDS]
        text = ' '.join(words)
        resp, _ = await ai.ask([
            {'role': 'system', 'content': SUMMARIZE_PROMPT},
            {'role': 'user', 'content': text}
        ], model=model)
        article = Article(
            source=self.source,
            url=url,
            title=title,
            summary=resp.get('summary'),
            companies=resp.get('companies'),
        )
        article.tax_list = []
        for prop_name, tax_type in [('industries', Taxonomy.TAX_TYPE_INDUSTRY), ('professions', Taxonomy.TAX_TYPE_PROFESSION)]:
            for name in resp.get(prop_name, []):
                article.tax_list.append((prop_name, tax_type, name))

        self.articles.append(article)

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
    source = 'Hacker News'

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

class TheRegister(ListArticleSource):
    source = 'The Register'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        BASE_URL = 'https://www.theregister.com'
        index_page_bs = self.web_reader.read_sync(BASE_URL)

        for article in index_page_bs.find_all('article'):
            sl = article.find('a', class_='story_link')
            if sl is None:
                continue
            url = BASE_URL + sl.get('href')
            if Article.objects.filter(url=url).exists():
                continue
            title = article.find('h4').text
            self.queue.append((url, title))

class TechCrunch(ListArticleSource):
    source = 'TechCrunch'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        BASE_URL = 'https://techcrunch.com/'
        index_page_bs = self.web_reader.read_sync(BASE_URL)

        articles = index_page_bs.find_all('article')
        for article in articles:
            a = article.find('a')
            if a is None:
                continue
            url = a.get('href')
            if url == BASE_URL:
                continue
            if Article.objects.filter(url=url).exists():
                continue
            title = a.text.strip()
            self.queue.append((url, title))

        for a in index_page_bs.find_all('a', class_='post-block__title__link'):
            url = a.get('href')
            if url == BASE_URL:
                continue
            if Article.objects.filter(url=url).exists():
                continue
            title = a.text.strip()
            self.queue.append((url, title))

article_source_classes = [HN, TheRegister, TechCrunch]
