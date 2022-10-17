from django.core.management import BaseCommand

from e2e_tests.db_setup import rebuild_db, write_db_to_file


class Command(BaseCommand):
    help = 'Populate the E2E DB or update the SQL build file for the DB'

    def add_arguments(self, parser):
        arg_group = parser.add_mutually_exclusive_group(required=True)
        arg_group.add_argument(
            '--rebuild', action='store_true',
            help='Rebuild the E2E database'
        )
        arg_group.add_argument(
            '--export', action='store_true',
            help='Update the SQL file used to rebuild the database'
        )

    def handle(self, *args, **options):
        if options.get('rebuild'):
            rebuild_db()
            self.stdout.write(self.style.SUCCESS('Database rebuilt'))
        elif options.get('export'):
            write_db_to_file()
            self.stdout.write(self.style.SUCCESS('Database export complete'))
