from django.core.management import BaseCommand

from jvapp.apis.job import JobClassificationView


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Max number of jobs to bucketize',
        )

    def handle(self, *args, **options):
        limit = options['limit']
        JobClassificationView.classify_jobs(limit)
