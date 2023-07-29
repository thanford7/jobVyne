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
        parser.add_argument(
            '--employer_limit',
            type=int,
            help='Max number of employers to summarize',
        )

    def handle(self, *args, **options):
        job_limit = options['job_limit']
        employer_limit = options['employer_limit']
        EmployerInfoView.fill_employer_info(limit=employer_limit)
        JobClassificationView.classify_jobs(job_limit, is_test=False)
