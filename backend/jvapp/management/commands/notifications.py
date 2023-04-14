import datetime
from collections import defaultdict
from datetime import timedelta
from time import sleep

from django.core.management import BaseCommand
from django.db.models import ExpressionWrapper, Q, fields
from django.db.models.functions import TruncDate

from jvapp.models.user import UserSocialCredential
from jvapp.utils.cron_util import CronPattern, get_datetime_to_nearest_minutes, get_seconds_to_next_minute_interval
from jvapp.utils.datetime import get_current_datetime
from jvapp.utils.email import send_django_email
from jvapp.utils.gmail import GmailAPIService
from jvapp.utils.oauth import OAUTH_CFGS, OauthProviders

MINUTES_PER_RUN = 10
EXPIRATION_DAY_FILTER = (7, 3, 0, -7)  # Number of days to expiration when notification should be sent
notify_expiring_social_credentials_cron = CronPattern(None, None, None, 12, 0)  # Equivalent to 7 am eastern


def get_expiring_social_credentials(expiration_days_filter: tuple):
    expiration_days = ExpressionWrapper(TruncDate('expiration_dt') - get_current_datetime().date(), output_field=fields.DurationField())
    
    # Create a filter for any of the expiration days specified
    days_filter = None
    for days in expiration_days_filter:
        filter_expression = Q(expiration_days=timedelta(days=days))
        if not days_filter:
            days_filter = filter_expression
        else:
            days_filter |= filter_expression
    
    # Google is only used for login so expiration doesn't matter
    platform_filter = ~Q(provider=OauthProviders.google.value)
    
    return UserSocialCredential.objects\
        .select_related('user')\
        .annotate(expiration_days=expiration_days)\
        .filter(platform_filter)\
        .filter(days_filter)


def get_serialized_expiring_social_credential(social_credential):
    return {
        'user_email': social_credential.user.email,
        'social_email': social_credential.email,
        'platform_name': OAUTH_CFGS[social_credential.provider]['name'],
        'user_full_name': social_credential.user.full_name,
        'expiration_date': social_credential.expiration_dt.date(),
        'expiration_days': social_credential.expiration_days.days
    }


class Command(BaseCommand):
    help = 'Send notifications on periodic intervals'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='Run once without cron',
        )
    
    def handle(self, *args, **options):
        gmail_api = GmailAPIService()
        if options['test']:
            self.send_credential_notifications(True)
            gmail_api.start_pub_sub_watch()
        else:
            last_gmail_service_date = False
            while True:
                current_date = datetime.date.today()
                if not last_gmail_service_date or (current_date != last_gmail_service_date):
                    gmail_api.start_pub_sub_watch()
                    last_gmail_service_date = current_date
                self.send_credential_notifications(False)
                seconds_to_next_run = get_seconds_to_next_minute_interval(MINUTES_PER_RUN)
                self.stdout.write(f'Waiting {seconds_to_next_run / 60} minutes for next run')
                sleep(seconds_to_next_run)
            
    def send_credential_notifications(self, is_test):
        writer = self.stdout.write
        current_dt = get_current_datetime()
        writer(f'Sending notifications at {current_dt}')
        rounded_dt = get_datetime_to_nearest_minutes(current_dt, MINUTES_PER_RUN)
        if notify_expiring_social_credentials_cron.is_match(rounded_dt) or is_test:
            expiring_social_credentials = [
                get_serialized_expiring_social_credential(esc)
                for esc in get_expiring_social_credentials(EXPIRATION_DAY_FILTER)
            ]
        
            # Group by user email so we only send one email even if multiple credentials are expiring
            grouped_expiring_social_credentials = defaultdict(list)
            for cred in expiring_social_credentials:
                grouped_expiring_social_credentials[cred['user_email']].append(cred)
            
            for email, creds in grouped_expiring_social_credentials.items():
                send_django_email(
                    'Expiring Social Credentials',
                    'emails/expiring_credential_email.html',
                    to_email=email,
                    django_context={
                        'user_full_name': creds[0]['user_full_name'],
                        'credentials': creds,
                        'is_exclude_final_message': True,
                        'is_unsubscribe': True
                    },
                    is_tracked=False
                )
            email_count = len(grouped_expiring_social_credentials.values())
            credential_count = len(expiring_social_credentials)
            writer(self.style.SUCCESS(f'Sent {email_count} emails for {credential_count} expiring credentials'))
