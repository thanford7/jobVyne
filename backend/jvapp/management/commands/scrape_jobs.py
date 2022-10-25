from django.core.management import BaseCommand

from scraper.scraper.runSpiders import run_crawlers


class Command(BaseCommand):
    help = 'Scrape job data from websites'

    def handle(self, *args, **options):
        run_crawlers()
        self.stdout.write(self.style.SUCCESS('Completed scrapy job data'))
