from django.core.management import BaseCommand

from e2e_tests.db_setup import rebuild_db, write_db_to_file
from jvapp.utils.taxonomy import run_job_title_standardization, update_taxonomies


class Command(BaseCommand):
    help = 'Update the taxonomy objects'

    def add_arguments(self, parser):
        parser.add_argument(
            '--is_non_standardized_only', action='store_true',
            help='Whether to only update for jobs that have not been standardized yet'
        )

    def handle(self, *args, **options):
        update_taxonomies()
        run_job_title_standardization(is_non_standardized_only=options.get('is_non_standardized_only'))
        self.stdout.write(self.style.SUCCESS('Jobs standardized'))
