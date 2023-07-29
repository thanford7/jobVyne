from django.core.management import BaseCommand

from jvapp.apis.employer import EmployerInfoView


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--limit_employer_info',
            type=int,
            help='Max number of employers to fill info for',
        )
        parser.add_argument(
            '--limit_employer_description',
            type=int,
            help='Max number of employers to fill description for',
        )

    def handle(self, *args, **options):
        limit_employer_info = options['limit_employer_info']
        limit_employer_description = options['limit_employer_description']
        EmployerInfoView.fill_employer_info(limit=limit_employer_info)
        EmployerInfoView.fill_employer_description(limit=limit_employer_description)
