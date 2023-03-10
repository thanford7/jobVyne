from time import sleep

from django.core.management import BaseCommand

from scrape.scraper import run_job_scrapers


class Command(BaseCommand):
    help = 'Scrape job data from websites'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--schedule_minutes',
            type=int,
            help='Minutes between when task is run',
        )

    def handle(self, *args, **options):
        writer = self.stdout.write
        schedule_minutes = options['schedule_minutes']
        if schedule_minutes:
            while True:
                writer('Running job scraping')
                run_job_scrapers(employer_names=None)
                writer(f'Waiting {schedule_minutes} minutes for next run')
                sleep(schedule_minutes * 60)
        else:
            run_job_scrapers(employer_names=None)
            self.stdout.write(self.style.SUCCESS('Completed scraping job data'))
