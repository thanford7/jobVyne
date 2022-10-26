from crontab import CronTab
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Adds demo data to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--scrape',
            action='store_true',
            help='Run job scraper',
        )
        parser.add_argument(
            '--ats',
            action='store_true',
            help='Run ATS job pull',
        )

    def handle(self, *args, **options):
        cron = CronTab(user='root')
        if options['scrape']:
            job = cron.new(command='python manage.py scrape_jobs')
            job.minute.every(5)
        cron.write()
        self.stdout.write(self.style.SUCCESS('Added cron jobs'))
