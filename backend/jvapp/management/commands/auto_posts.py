import logging
from time import sleep

from django.core.management import BaseCommand

from jvapp.apis.content import ShareSocialPostView
from jvapp.apis.slack import SlackJobSeekerJobsView, SlackJobsMessageView, SlackReferralsMessageView
from jvapp.utils.cron_util import get_datetime_to_nearest_minutes, get_seconds_to_next_minute_interval
from jvapp.utils.datetime import get_current_datetime

logger = logging.getLogger(__name__)
MINUTES_PER_RUN = 15


class Command(BaseCommand):
    help = 'Auto-post to social media profiles'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--test_dt',
            type=str,
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
                    logger.error(error)
                    
                writer(self.style.SUCCESS(f'{successful_posts} successful social posts'))
                
                successful_slack_job_posts = SlackJobsMessageView.run_auto_posts(current_dt)
                writer(self.style.SUCCESS(f'{successful_slack_job_posts} successful Slack job posts'))

                successful_slack_referral_posts = SlackReferralsMessageView.run_auto_posts()
                writer(self.style.SUCCESS(f'{successful_slack_referral_posts} successful Slack referral posts'))

                successful_slack_job_seeker_posts = SlackJobSeekerJobsView.send_job_slack_messages(current_dt)
                writer(self.style.SUCCESS(f'{successful_slack_job_seeker_posts} successful Slack job seeker posts'))
