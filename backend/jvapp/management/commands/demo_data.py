from django.core.management import BaseCommand

from demoData import create_ancillary_data, create_recurring_data, delete_demo_employers
from jvapp.utils.taxonomy import run_job_title_standardization, update_taxonomies


class Command(BaseCommand):
    help = 'Adds demo data to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ancillary',
            action='store_true',
            help='Include ancillary data',
        )
        parser.add_argument(
            '--is_delete_existing',
            action='store_true',
            help='Delete demo employers before creating new data',
        )

    def handle(self, *args, **options):
        if options['is_delete_existing']:
            delete_demo_employers()
            
        if options['ancillary']:
            create_ancillary_data()
        create_recurring_data()
        update_taxonomies()
        run_job_title_standardization(is_non_standardized_only=True)
        self.stdout.write(self.style.SUCCESS('Updated demo data'))