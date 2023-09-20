import logging
from django.core.management import BaseCommand

from jvapp.apis.articles.summarize import pull_articles

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
        pull_articles(limit)
