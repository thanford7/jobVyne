import datetime
from time import sleep

from django.core.management import BaseCommand

from jvapp.apis.content import ShareSocialPostView
from jvapp.utils.cron_util import get_datetime_to_nearest_minutes, get_seconds_to_next_minute_interval
from jvapp.utils.datetime import get_current_datetime


MINUTES_PER_RUN = 15


class Command(BaseCommand):
    help = 'Auto-post to social media profiles'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--test_dt',
            type=datetime.datetime,
            help='A specific datetime to use as a test trigger for auto-posts',
        )
    
    def handle(self, *args, **options):
        writer = self.stdout.write
        test_dt = options['test_dt']
        if test_dt:
            writer(f'Testing auto-posts with {test_dt} datetime')
        else:
            while True:
                seconds_to_next_run = get_seconds_to_next_minute_interval(MINUTES_PER_RUN)
                writer(f'Waiting {seconds_to_next_run / 60} minutes for next run')
                sleep(seconds_to_next_run)
                current_dt = get_current_datetime()
                writer(f'Sending auto-posts at {current_dt}')
                
                # Make sure time is on the 15-minute mark
                current_dt = get_datetime_to_nearest_minutes(current_dt, MINUTES_PER_RUN)
                writer(f'Using target datetime of {current_dt}')
                # Send out posts
                errors, successful_posts = ShareSocialPostView.run_auto_posts(current_dt)
                for error in errors:
                    writer(self.style.ERROR(error))
                writer(self.style.SUCCESS(f'{successful_posts} successful posts'))