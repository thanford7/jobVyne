import logging
from django.core.management import BaseCommand

from jvapp.apis.events.pull import pull_events

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Pull events from defined websites'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit the number of events to pull',
        )

    def handle(self, *args, **options):
        limit = options['limit']
        pull_events(limit)
