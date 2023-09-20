from django.core.management import BaseCommand
from django.db.models import Q

from jvapp.models.user import UserConnection


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--is_exclude_profession',
            type=bool
        )
        parser.add_argument(
            '--is_exclude_employer',
            type=bool,
        )
        parser.add_argument(
            '--is_null_only',
            type=bool,
        )

    def handle(self, *args, **options):
        is_null_only = options.get('is_null_only')
        is_exclude_employer = options.get('is_exclude_employer')
        is_exclude_profession = options.get('is_exclude_profession')
        
        