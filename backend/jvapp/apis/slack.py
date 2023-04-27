import hashlib
import hmac
import json
import logging
from datetime import timedelta
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.conf import settings
from django.core.files import File
from django.db.models import F, Q
from django.db.transaction import atomic
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from slack_sdk import WebClient

from jobVyne.multiPartJsonParser import RawFormParser
from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY, get_error_response
from jvapp.apis.employer import EmployerJobView, EmployerSlackView
from jvapp.apis.social import SocialLinkFilterView
from jvapp.models import EmployerSlack, JobVyneUser, PermissionName, SocialLinkFilter
from jvapp.models.content import JobPost
from jvapp.permissions.employer import IsAdminOrEmployerPermission
from jvapp.utils.data import coerce_int
from jvapp.utils.datetime import WEEKDAY_BITS, get_datetime_format_or_none, get_datetime_minutes, get_dow_bit, \
    get_unix_datetime
from jvapp.utils.slack import raise_slack_exception_if_error

logger = logging.getLogger(__name__)
SLACK_BASE_URL = 'https://slack.com/api/'


class SlackBaseView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.employer_id = coerce_int(self.query_params.get('employer_id') or self.data.get('employer_id'))
        self.slack_cfg = EmployerSlackView.get_slack_cfg(self.employer_id)
    
    def is_bad_request(self):
        if not self.employer_id:
            return get_error_response('An employer ID is required')
        if not self.user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_SETTINGS.value, self.employer_id):
            return get_error_response('You do not have permission for this operation')
        if not any((self.slack_cfg, self.slack_cfg.oauth_key)):
            return get_error_response('No current Slack configuration')
        return False
    
    @staticmethod
    def get_slack_client(slack_cfg):
        return WebClient(token=slack_cfg.oauth_key)
    
    @staticmethod
    def get_user_profile(user_key, slack_client: WebClient):
        resp = slack_client.users_profile_get(user=user_key)
        raise_slack_exception_if_error(resp)
        return resp['profile']
    
    @staticmethod
    def get_profile_picture(slack_user_profile):
        profile_picture_url = slack_user_profile.get('image_512')
        if not profile_picture_url:
            return None
        profile_picture = NamedTemporaryFile()
        profile_picture.write(urlopen(profile_picture_url).read())
        profile_picture.flush()
        return profile_picture
    
    @staticmethod
    def get_or_create_jobvyne_user(slack_user_profile, employer_id):
        try:
            user_filter = Q(employer_id=employer_id)
            user_filter &= (Q(email=slack_user_profile['email']) | Q(business_email=slack_user_profile['email']))
            user = JobVyneUser.objects.get(user_filter)
            is_updated = False
            if not user.user_type_bits & JobVyneUser.USER_TYPE_EMPLOYEE:
                user.user_type_bits |= JobVyneUser.USER_TYPE_EMPLOYEE
                is_updated = True
            if (not user.profile_picture) and (
            profile_picture := SlackBaseView.get_profile_picture(slack_user_profile)):
                user.profile_picture = File(profile_picture, name='slack_profile_512.png')
                is_updated = True
            if is_updated:
                user.save()
        except JobVyneUser.DoesNotExist:
            profile_picture = SlackBaseView.get_profile_picture(slack_user_profile)
            user = JobVyneUser.objects.create_user(
                slack_user_profile['email'],
                user_type_bits=JobVyneUser.USER_TYPE_EMPLOYEE,
                first_name=slack_user_profile['first_name'],
                last_name=slack_user_profile['last_name'],
                phone_number=slack_user_profile['phone'],
                employer_id=employer_id,
                profile_picture=File(profile_picture, name='slack_profile_512') if profile_picture else None
            )
        
        return user
    

class SlackJobsMessageView(SlackBaseView):
    # Jobs later than this will not be posted
    JOB_LOOKBACK_DAYS = 14
    MAX_JOBS = 5
    DEFAULT_DOW_BITS = WEEKDAY_BITS
    DEFAULT_TIME_OF_DAY_MINUTES = 12 * 60
    
    def post(self, request):
        if bad_request := self.is_bad_request():
            return bad_request
        self.send_slack_job_post(self.slack_cfg, self.data.get('is_test', True))
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Slack message posted'
        })
    
    @staticmethod
    def run_auto_posts(target_dt):
        target_dow = get_dow_bit(target_dt)
        target_tod = get_datetime_minutes(target_dt)
        is_default_dow = bool(target_dow & SlackJobsMessageView.DEFAULT_DOW_BITS)
        is_default_tod = target_tod == SlackJobsMessageView.DEFAULT_TIME_OF_DAY_MINUTES
        dow_filter = Q(
            jobs_post_dow_bits__lt=F('jobs_post_dow_bits') + (1 * F('jobs_post_dow_bits').bitand(target_dow)))
        if is_default_dow:
            post_filter = (
                    Q(jobs_post_dow_bits__isnull=True) | dow_filter
            )
        else:
            post_filter = dow_filter
        
        tod_filter = Q(jobs_post_tod_minutes=target_tod)
        if is_default_tod:
            post_filter &= (Q(jobs_post_tod_minutes__isnull=True) | tod_filter)
        else:
            post_filter &= tod_filter
        
        slack_cfgs = EmployerSlack.objects.select_related('employer').filter(
            is_enabled=True,
            jobs_post_channel__isnull=False
        ).filter(post_filter)
        successful_posts = 0
        for slack_cfg in slack_cfgs:
            is_success = SlackJobsMessageView.send_slack_job_post(slack_cfg)
            if is_success:
                successful_posts += 1
        
        return successful_posts
    
    @staticmethod
    @atomic
    def send_slack_job_post(slack_cfg, is_test):
        if not slack_cfg.jobs_post_channel:
            logger.warning('No Slack channel set to post jobs to')
            return False
        jobs = SlackJobsMessageView.get_jobs_for_post(slack_cfg.employer_id, slack_cfg)
        if not jobs:
            logger.info('No new jobs to post to Slack')
            return False
        
        client = SlackBaseView.get_slack_client(slack_cfg)
        jobs_message = SlackJobsMessageView.build_jobs_message(jobs, slack_cfg.employer)
        resp = client.chat_postMessage(
            channel=slack_cfg.jobs_post_channel,
            blocks=json.dumps(jobs_message)
        )
        raise_slack_exception_if_error(resp)
        if not is_test:
            job_posts = []
            for job in jobs:
                job_posts.append(
                    JobPost(
                        employer_id=slack_cfg.employer_id,
                        job_id=job.id,
                        channel=JobPost.PostChannel.SLACK_JOB.value,
                        created_dt=timezone.now(),
                        modified_dt=timezone.now()
                    )
                )
            JobPost.objects.bulk_create(job_posts)
        return True
    
    @staticmethod
    def get_jobs_for_post(employer_id, slack_cfg):
        jobs_filter = Q(employer_id=employer_id)
        # Don't post jobs that have already been posted
        jobs_filter &= (
                Q(job_post__isnull=True) | ~Q(job_post__channel=JobPost.PostChannel.SLACK_JOB.value)
        )
        # Only post recent jobs
        jobs_filter &= Q(open_date__gte=timezone.now().date() - timedelta(days=SlackJobsMessageView.JOB_LOOKBACK_DAYS))
        job_count = min(slack_cfg.jobs_post_max_jobs or SlackJobsMessageView.MAX_JOBS, SlackJobsMessageView.MAX_JOBS)
        return EmployerJobView.get_employer_jobs(employer_job_filter=jobs_filter)[:job_count]
    
    @staticmethod
    def build_jobs_message(jobs, employer):
        blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': ':grapes: JobVyne has a fresh batch of jobs ready to be plucked and enjoyed with a fresh glass of "get hired".'
                }
            },
            {'type': 'divider'},
        ]
        
        for job in jobs:
            job_link = SocialLinkFilter()
            job_link, _ = SocialLinkFilterView.create_or_update_link_filter(job_link, {
                'employer_id': employer.id,
                'job_ids': [job.id]
            })
            job_info = {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f'*Job title:*\n<{job_link.get_link_url(platform_name="slack")}|{job.job_title}>'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*Company:*\n{job.employer.employer_name}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*Location:*\n{job.get_locations_text()}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*Salary:*\n{job.get_salary_text()}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*Post date:*\n{get_datetime_format_or_none(job.open_date)}'
                    }
                ],
            }
            if job.employer.logo:
                job_info['accessory'] = {
                    'type': 'image',
                    'image_url': job.employer.logo.url,
                    'alt_text': f'{job.employer.employer_name} logo'
                }
            
            # TODO: Add actions for:
            #  user to indicate they work at the given company
            #  user to follow company
            # job_actions = {
            #     'type': 'actions',
            #     'elements': [
            #         {
            #             'type': 'button',
            #             'text': {
            #                 'type': 'plain_text',
            #                 'emoji': True,
            #                 'text': 'View job'
            #             },
            #             'style': 'primary',
            #             'url': '',
            #             'action_id': 'jv-work-here'
            #         },
            #     ]
            # }
            blocks.append(job_info)
        
        general_job_link = SocialLinkFilter()
        general_job_link, _ = SocialLinkFilterView.create_or_update_link_filter(general_job_link, {
            'employer_id': employer.id,
            'name': 'Slack bot'
        })
        
        blocks.append({'type': 'divider'})
        blocks.append({
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'*<{general_job_link.get_link_url(platform_name="slack")}|View all open jobs>*'
            }
        })
        
        return blocks


class SlackReferralsMessageView(SlackBaseView):
    
    def post(self, request):
        if bad_request := self.is_bad_request():
            return bad_request
        self.send_slack_referral_post(self.slack_cfg, self.data.get('is_test', True))
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Slack message posted'
        })
    
    @staticmethod
    @atomic
    def send_slack_referral_post(slack_cfg, is_test):
        jobs = SlackReferralsMessageView.get_jobs_for_post(slack_cfg.employer_id)
        if is_test:
            jobs = jobs[:1]
        
        client = SlackBaseView.get_slack_client(slack_cfg)
        for job in jobs:
            jobs_message = SlackReferralsMessageView.build_referral_message(job, slack_cfg)
            resp = client.chat_postMessage(
                channel=slack_cfg.jobs_post_channel,
                blocks=json.dumps(jobs_message)
            )
            raise_slack_exception_if_error(resp)
        
        if not is_test:
            job_posts = []
            for job in jobs:
                job_posts.append(
                    JobPost(
                        employer_id=slack_cfg.employer_id,
                        job_id=job.id,
                        channel=JobPost.PostChannel.SLACK_EMPLOYEE_REFERRAL.value,
                        created_dt=timezone.now(),
                        modified_dt=timezone.now()
                    )
                )
            JobPost.objects.bulk_create(job_posts)
        return True
    
    @staticmethod
    def get_jobs_for_post(employer_id):
        jobs_filter = Q(employer_id=employer_id)
        # Don't post jobs that have already been posted
        jobs_filter &= (
                Q(job_post__isnull=True) | ~Q(job_post__channel=JobPost.PostChannel.SLACK_EMPLOYEE_REFERRAL.value)
        )
        # Only post recent jobs
        jobs_filter &= Q(open_date__gte=timezone.now().date() - timedelta(days=SlackJobsMessageView.JOB_LOOKBACK_DAYS))
        return EmployerJobView.get_employer_jobs(employer_job_filter=jobs_filter)
    
    @staticmethod
    def build_referral_message(job, slack_cfg):
        blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': ':grapes: New job referral opportunity.'
                }
            },
            {'type': 'divider'},
        ]

        job_link = SocialLinkFilter()
        job_link, _ = SocialLinkFilterView.create_or_update_link_filter(job_link, {
            'employer_id': slack_cfg.employer_id,
            'job_ids': [job.id]
        })
        
        job_info = {
            'type': 'section',
            'fields': [
                {
                    'type': 'mrkdwn',
                    'text': f'*Job title:*\n<{job_link.get_link_url(platform_name="slack")}|{job.job_title}>'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*Location:*\n{job.get_locations_text()}'
                }
            ],
        }
        
        button_value = {
            'employer_slack_id': slack_cfg.id,
            'employer_id': slack_cfg.employer_id,
            'job_id': job.id
        }
        
        job_actions = {
            'type': 'actions',
            'elements': [
                {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'emoji': True,
                        'text': 'Share job'
                    },
                    'style': 'primary',
                    'value': json.dumps(button_value),
                    'action_id': 'jv-referral'
                },
            ]
        }
        blocks.append(job_info)
        blocks.append(job_actions)
        
        return blocks


class SlackWebhookInboundView(JobVyneAPIView):
    permission_classes = [AllowAny]
    parser_classes = [RawFormParser]
    
    def post(self, request):
        if not self.is_valid_slack_request(request):
            return Response(status=status.HTTP_403_FORBIDDEN, data='Invalid request signature')
        data = json.loads(request.data['payload'])
        button_data = json.loads(data['actions'][0]['value'])
        slack_cfg = EmployerSlackView.get_slack_cfg(button_data['employer_id'])
        slack_client = SlackBaseView.get_slack_client(slack_cfg)
        slack_user_profile = SlackBaseView.get_user_profile(data['user']['id'], slack_client)
        user = SlackBaseView.get_or_create_jobvyne_user(slack_user_profile, slack_cfg.employer_id)
        job = EmployerJobView.get_employer_jobs(employer_job_id=button_data['job_id'])
        job_referral_link = SocialLinkFilter()
        job_referral_link, _ = SocialLinkFilterView.create_or_update_link_filter(job_referral_link, {
            'owner_id': user.id,
            'employer_id': slack_cfg.employer_id,
            'job_ids': [job.id]
        })
        
        resp = slack_client.views_open(
            trigger_id=data['trigger_id'],
            view={
                'type': 'modal',
                'callback_id': 'jobvyne-referral-link',
                'title': {
                    'type': 'plain_text',
                    'text': 'Job referral link'
                },
                'blocks': [
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': f'*Unique referral link for {job.job_title}:*'
                        }
                    },
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': f'{job_referral_link.get_link_url(platform_name="slack")}'
                        }
                    },
                    {'type': 'divider'},
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': 'You can copy this link and share it anywhere. Anyone that applies using this link will be considered your referral. You will be notified by email whenever you get a new referral.'
                        }
                    },
                ],
            }
        )
        return Response(status=status.HTTP_200_OK)
    
    @staticmethod
    def is_valid_slack_request(request):
        # verifier = SignatureVerifier(signing_secret=settings.SLACK_SIGNING_SECRET)
        timestamp = int(request.headers['X-Slack-Request-Timestamp'])
        current_timestamp = get_unix_datetime(timezone.now())
        if abs(current_timestamp - timestamp) > 60 * 5:
            # The request timestamp is more than five minutes from local time.
            # It could be a replay attack, so let's ignore it.
            return
        
        sig_basestring = 'v0:' + str(timestamp) + ':' + request.data['_raw_data']
        signature = 'v0=' + hmac.new(
            key=settings.SLACK_SIGNING_SECRET.encode('utf-8'),
            msg=sig_basestring.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        slack_signature = request.headers['X-Slack-Signature']
        return hmac.compare_digest(signature, slack_signature)


class SlackChannelView(SlackBaseView):
    
    def get(self, request):
        if bad_request := self.is_bad_request():
            return bad_request
        client = self.get_slack_client(self.slack_cfg)
        resp = client.conversations_list(exclude_archived=True)
        raise_slack_exception_if_error(resp)
        channels = [{'key': c['id'], 'name': c['name']} for c in resp['channels']]
        channels.sort(key=lambda c: c['name'])
        return Response(status=status.HTTP_200_OK, data=channels)
