from django.core.management import BaseCommand

from jvapp.apis.employer import EmployerInfoView
from jvapp.apis.job import JobClassificationView


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--job_limit',
            type=int,
            help='Max number of jobs to bucketize',
        )

    def handle(self, *args, **options):
        job_limit = options['job_limit']
        JobClassificationView.classify_jobs(job_limit, is_test=False)
