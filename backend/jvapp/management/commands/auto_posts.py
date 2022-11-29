import datetime
from time import sleep

from django.core.management import BaseCommand

from jvapp.apis.content import ShareSocialPostView
from jvapp.utils.data import round_to
from jvapp.utils.datetime import get_current_datetime


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
                seconds_to_next_run = self.get_seconds_to_next_run()
                writer(f'Waiting {seconds_to_next_run / 60} minutes for next run')
                sleep(seconds_to_next_run)
                current_dt = get_current_datetime()
                writer(f'Sending auto-posts at {current_dt}')
                
                # Make sure time is on the 15-minute mark
                round_15 = round_to(current_dt.minute, 15)
                current_dt = current_dt + datetime.timedelta(minutes=round_15 - current_dt.minute)
                current_dt = current_dt.replace(second=0, microsecond=0)
                writer(f'Using target datetime of {current_dt}')
                # Send out posts
                errors, successful_posts = ShareSocialPostView.run_auto_posts(current_dt)
                for error in errors:
                    writer(self.style.ERROR(error))
                writer(self.style.SUCCESS(f'{successful_posts} successful posts'))
    
    @staticmethod
    def get_seconds_to_next_run():
        # Since we can deploy at any time we need to sync up
        # with the 15-minute marks (xx:00, xx:15, xx:30, xx:45)
        current_utc_dt = get_current_datetime()
        target_utc_dt = get_current_datetime().replace(second=0, microsecond=0)
        # Add the number of minutes to get to the next 15 minute mark
        target_utc_dt = target_utc_dt + datetime.timedelta(minutes=15 - (target_utc_dt.minute % 15))
        return (target_utc_dt - current_utc_dt).total_seconds()