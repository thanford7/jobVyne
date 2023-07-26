from django.core.management import BaseCommand

from jvapp.apis.employer import EmployerInfoView


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Max number of companies to fill',
        )

    def handle(self, *args, **options):
        limit = options['limit']
        EmployerInfoView.fill_company_info(limit)
