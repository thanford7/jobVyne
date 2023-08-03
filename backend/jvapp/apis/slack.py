import hashlib
import hmac
import json
import logging
from typing import Union

from django.conf import settings
from django.db.models import F, Q
from django.db.transaction import atomic
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from slack_sdk import WebClient

from jobVyne.multiPartJsonParser import RawFormParser
from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY, get_error_response
from jvapp.apis.employer import EmployerJobView, EmployerSlackView
from jvapp.apis.job_subscription import JobSubscriptionView
from jvapp.apis.social import SocialLinkPostJobsView, SocialLinkView
from jvapp.models.content import JobPost
from jvapp.models.employer import Employer, EmployerJobConnection, EmployerSlack
from jvapp.models.social import SocialLink
from jvapp.models.user import JobVyneUser, PermissionName, UserSocialSubscription
from jvapp.permissions.employer import IsAdminOrEmployerPermission
from jvapp.utils.data import coerce_int
from jvapp.utils.datetime import WEEKDAY_BITS, get_datetime_format_or_none, get_datetime_minutes, get_dow_bit, \
    get_unix_datetime
from jvapp.utils.email import EMAIL_ADDRESS_SUPPORT, send_django_email
from jvapp.utils.image import convert_url_to_image
from jvapp.utils.oauth import OauthProviders
from jvapp.utils.slack import raise_slack_exception_if_error
from jvapp.slack.slack_blocks import InputOption, Modal, SelectEmployer
from jvapp.slack.slack_modals import JobModalViews, JobSeekerModalViews

logger = logging.getLogger(__name__)
SLACK_BASE_URL = 'https://slack.com/api/'


class SlackBasePoster:
    MAX_JOBS_DEFAULT = 10
    IS_PER_JOB_POST = False
    
    def __init__(
            self, slack_cfg, post_channel,
            employer_id=None, owner_id=None, recipient_id=None, max_jobs: int = None, is_test: bool = False,
            message_data=None, slack_user_id=None
    ):
        assert any((employer_id, owner_id))
        assert not all((employer_id, owner_id))
        self.max_jobs = max_jobs or self.MAX_JOBS_DEFAULT
        self.slack_cfg = slack_cfg
        self.post_channel = post_channel
        self.employer_id = employer_id
        self.owner_id = owner_id
        self.recipient_id = recipient_id
        self.is_test = is_test
        self.client = SlackBaseView.get_slack_client(self.slack_cfg)
        self.message_data = message_data or {}
        self.slack_user_id = slack_user_id
    
    @atomic
    def send_slack_job_post(self, *args, **kwargs) -> Union[str, None]:
        """Return False if the post was successful"""
        if error_msg := self.has_error():
            return error_msg
        
        jobs = self.get_jobs_for_post(*args, **kwargs)
        if not jobs and not self.is_test:
            msg = 'No new jobs to post to Slack'
            logger.info(msg)
            return msg
        
        job_posts = []
        if self.IS_PER_JOB_POST:
            for job in jobs:
                message = self.build_message(job, **self.message_data)
                resp = self._send_slack_post(message)
                raise_slack_exception_if_error(resp)
                job_posts.append(self.generate_job_post(job, resp, message))
        else:
            message = self.build_message(jobs, **self.message_data)
            resp = self._send_slack_post(message)
            raise_slack_exception_if_error(resp)
            for job in jobs:
                job_posts.append(self.generate_job_post(job, resp, message))
        
        if not self.is_test:
            JobPost.objects.bulk_create(job_posts)
    
    def get_jobs_for_post(self, *args, **kwargs):
        return SocialLinkPostJobsView.get_jobs_for_post(
            self.max_jobs, self.post_channel,
            employer_id=self.employer_id, owner_id=self.owner_id, recipient_id=self.recipient_id
        )
    
    def generate_job_post(self, job, resp, message_blocks):
        meta_data = {
            'message_blocks': message_blocks,
            'ts': resp['ts'],
            'channel': resp['channel'],
            'message': resp['message']
        }
        return JobPost(
            employer_id=self.employer_id,
            owner_id=self.owner_id,
            recipient_id=self.recipient_id,
            job_id=job.id,
            channel=self.post_channel,
            created_dt=timezone.now(),
            modified_dt=timezone.now(),
            meta_data=meta_data
        )
    
    def build_message(self, jobs, **kwargs):
        return NotImplementedError()
    
    def has_error(self):
        return None
    
    def _send_slack_post(self, message):
        return self.client.chat_postMessage(
            channel=self.slack_cfg.jobs_post_channel,
            blocks=json.dumps(message),
            unfurl_links=False
        )
    
    def _get_slack_message_jobs_list(self, jobs):
        blocks = []
        for job in jobs:
            job_link = SocialLinkView.get_or_create_single_job_link(job, employer_id=self.slack_cfg.employer.id)
            
            job_info = {
                'type': 'section',
                'block_id': f'jobs-list-summary-{job.id}',
                'text': {
                    'type': 'mrkdwn',
                    'text': (
                        f'*<{job_link.get_link_url(platform_name="slack")}|{job.job_title}>*\n'
                        f'*{job.employer.employer_name}*\n'
                        f'{job.employer.description if job.employer.description else ""}'
                    )
                }
            }
            if job.employer.logo_square_88:
                job_info['accessory'] = {
                    'type': 'image',
                    'image_url': job.employer.logo_square_88.url,
                    'alt_text': f'{job.employer.employer_name} logo'
                }
            
            blocks.append(job_info)
            
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
            
            job_details = {
                'type': 'section',
                'block_id': f'jobs-list-details-{job.id}',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f'*Location:*\n{job.locations_text}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*Salary:*\n{job.salary_text}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*Post date:*\n{get_datetime_format_or_none(job.open_date)}'
                    }
                ],
            }
            
            blocks.append(job_details)
            blocks.append({'type': 'divider'})
        
        general_job_link = SocialLink.objects.get(employer_id=self.slack_cfg.employer.id, owner_id__isnull=True,
                                                  is_default=True)
        blocks.append({
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'*<{general_job_link.get_link_url(platform_name="slack")}|View all open jobs>*'
            }
        })
        return blocks


class SlackJobPoster(SlackBasePoster):
    
    def has_error(self):
        if not self.slack_cfg.jobs_post_channel:
            msg = 'No Slack channel set to post jobs to'
            logger.warning(msg)
            return msg
        return False
    
    def build_message(self, jobs, **kwargs):
        blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': (
                        ':grapes: JobVyne has a fresh batch of jobs ready to be plucked and enjoyed with a fresh glass of "get hired".\n'
                        'Have a job you want to post? Use `/jv-job`'
                    )
                }
            },
            {'type': 'divider'},
            *self._get_slack_message_jobs_list(jobs)
        ]
        return blocks


class SlackUserGeneratedJobPoster(SlackBasePoster):
    
    def get_jobs_for_post(self, job, *args, **kwargs):
        try:
            # Check if job has already been posted
            existing_job_post = JobPost.objects.get(
                job=job, employer_id=self.employer_id, channel=self.post_channel
            )
            return None
        except JobPost.DoesNotExist:
            return [job]
    
    def build_message(self, jobs, slack_user_profile=None, job_connection=None, **kwargs):
        assert slack_user_profile and job_connection
        connection_descriptions = {
            EmployerJobConnection.ConnectionTypeBit.HIRING_MEMBER.value: 'is part of the hiring team',
            EmployerJobConnection.ConnectionTypeBit.CURRENT_EMPLOYEE.value: 'works at the employer',
            EmployerJobConnection.ConnectionTypeBit.FORMER_EMPLOYEE.value: 'previously worked at the employer',
            EmployerJobConnection.ConnectionTypeBit.KNOW_EMPLOYEE.value: 'knows someone who works at the employer',
            EmployerJobConnection.ConnectionTypeBit.NO_CONNECTION.value: 'has no connection with the employer',
        }
        connection_description = connection_descriptions[job_connection.connection_type] + ' for this job'
        connection_details = [
            f'ℹ️ {slack_user_profile["first_name"]} {connection_description}'
        ]
        if job_connection.is_allow_contact:
            connection_details.append(
                f'🤝 {slack_user_profile["first_name"]} is open to inquiries about this job'
            )
        else:
            connection_details.append(
                f'❌ {slack_user_profile["first_name"]} is NOT open to inquiries about this job'
            )
        
        blocks = [
            {
                'type': 'section',
                'block_id': 'user_post_intro',
                'text': {
                    'type': 'mrkdwn',
                    'text': f':grapes: *<@{slack_user_profile["user_key"]}> just posted a new job!*'
                }
            },
            {
                'type': 'section',
                'block_id': 'user_post_details',
                'text': {
                    'type': 'mrkdwn',
                    'text': '\n'.join(connection_details)
                }
            },
            {'type': 'divider'},
            *self._get_slack_message_jobs_list(jobs)
        ]
        return blocks


class SlackReferralPoster(SlackBasePoster):
    IS_PER_JOB_POST = True
    
    def build_message(self, job, **kwargs):
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
        
        job_link = SocialLink()
        job_link = SocialLinkView.create_or_update_link(job_link, {
            'employer_id': self.slack_cfg.employer_id,
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
                    'text': f'*Location:*\n{job.locations_text}'
                }
            ],
        }
        
        button_value = {
            'employer_slack_id': self.slack_cfg.id,
            'employer_id': self.slack_cfg.employer_id,
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
    
    def get_jobs_for_post(self):
        jobs = super().get_jobs_for_post()
        if self.is_test:
            jobs = jobs[:1] if jobs else []
        return jobs


class SlackJobRecipientPoster(SlackBasePoster):
    
    def build_message(self, jobs, user=None, **kwargs):
        blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': ''.join((
                        f'👋 Hi {user.first_name}, we hope you\'re having an awesome day!\n',
                        ':grapes: JobVyne has a fresh batch of jobs ready to be plucked and enjoyed with a fresh glass of "get hired".'
                    ))
                }
            },
            {'type': 'divider'},
            *self._get_slack_message_jobs_list(jobs)
        ]
        return blocks
    
    def _send_slack_post(self, message):
        assert self.slack_user_id
        
        # Open a conversation with a specific user
        conversation_resp = self.client.conversations_open(
            users=self.slack_user_id,
        )
        raise_slack_exception_if_error(conversation_resp)
        
        # Send the user a message
        return self.client.chat_postMessage(
            channel=conversation_resp.data['channel']['id'],
            blocks=json.dumps(message),
            unfurl_links=False
        )


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
    def get_slack_client(slack_cfg=None, token=None):
        return WebClient(token=token or slack_cfg.oauth_key)
    
    @staticmethod
    def get_user_profile(user_key, slack_client: WebClient):
        resp = slack_client.users_profile_get(user=user_key)
        raise_slack_exception_if_error(resp)
        profile = resp['profile']
        profile['user_key'] = user_key
        return profile
    
    @staticmethod
    def get_profile_picture(slack_user_profile):
        profile_picture_url = slack_user_profile.get('image_512')
        return convert_url_to_image(profile_picture_url, 'slack_profile_512.png')
    
    @staticmethod
    def subscribe_user_to_groups(user: JobVyneUser, slack_cfg: EmployerSlack):
        if slack_cfg.employer.organization_type == Employer.ORG_TYPE_GROUP:
            user.membership_groups.add(slack_cfg.employer)
            job_subscriptions = JobSubscriptionView.get_job_subscriptions(employer_id=slack_cfg.employer_id)
            professions = JobSubscriptionView.get_combined_job_professions_from_subscriptions(job_subscriptions)
            user.membership_professions.add(*professions)
        else:
            user.membership_employers.add(slack_cfg.employer)
    
    @staticmethod
    def get_or_create_jobvyne_user(slack_user_profile, user_type_bits, slack_cfg, employer_id=None):
        try:
            user_filter = Q(email=slack_user_profile['email']) | Q(business_email=slack_user_profile['email'])
            user = (
                JobVyneUser.objects
                .prefetch_related(
                    'job_search_industries',
                    'job_search_professions'
                )
                .select_related('job_search_level')
                .get(user_filter)
            )
            is_updated = False
            if (user.user_type_bits & user_type_bits) != user_type_bits:
                user.user_type_bits |= user_type_bits
                is_updated = True
            if (not user.profile_picture) and (
                    profile_picture := SlackBaseView.get_profile_picture(slack_user_profile)
            ):
                user.profile_picture = profile_picture
                is_updated = True
            linkedin_url = slack_user_profile.get('linkedin_url')
            first_name = slack_user_profile['first_name']
            last_name = slack_user_profile['last_name']
            home_post_code = slack_user_profile.get('home_post_code')
            professional_site_url = slack_user_profile.get('professional_site_url')
            for val, attr in (
                    (linkedin_url, 'linkedin_url'),
                    (first_name, 'first_name'),
                    (last_name, 'last_name'),
                    (home_post_code, 'home_post_code'),
                    (professional_site_url, 'professional_site_url')
            ):
                if val and val != getattr(user, attr):
                    setattr(user, attr, val)
                    is_updated = True
            
            if employer_id:
                if user.employer_id and user.employer_id != employer_id:
                    raise ValueError('This user is already assigned to a different employer')
                elif not user.employer_id:
                    user.employer_id = employer_id
                    is_updated = True
            if is_updated:
                user.save()
        except JobVyneUser.DoesNotExist:
            profile_picture = SlackBaseView.get_profile_picture(slack_user_profile)
            user = JobVyneUser.objects.create_user(
                slack_user_profile['email'],
                user_type_bits=user_type_bits,
                first_name=slack_user_profile['first_name'],
                last_name=slack_user_profile['last_name'],
                phone_number=slack_user_profile['phone'],
                employer_id=employer_id,
                profile_picture=profile_picture
            )
        
        SlackBaseView.subscribe_user_to_groups(user, slack_cfg)
        
        return user


class SlackJobsMessageView(SlackBaseView):
    # Jobs later than this will not be posted
    MAX_JOBS = 5
    DEFAULT_DOW_BITS = WEEKDAY_BITS
    DEFAULT_TIME_OF_DAY_MINUTES = 12 * 60
    
    def post(self, request):
        if bad_request := self.is_bad_request():
            return bad_request
        slack_poster = self.get_slack_poster(self.slack_cfg, self.data.get('is_test', True))
        error_msg = slack_poster.send_slack_job_post()
        if error_msg:
            return get_error_response(error_msg)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Slack message posted'
        })
    
    @staticmethod
    def get_slack_poster(slack_cfg, is_test):
        return SlackJobPoster(
            slack_cfg, JobPost.PostChannel.SLACK_JOB.value,
            employer_id=slack_cfg.employer_id,
            is_test=is_test,
            max_jobs=min(slack_cfg.jobs_post_max_jobs or SlackJobsMessageView.MAX_JOBS, SlackJobsMessageView.MAX_JOBS)
        )
    
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
            slack_poster = SlackJobsMessageView.get_slack_poster(slack_cfg, False)
            error_msg = slack_poster.send_slack_job_post()
            if not error_msg:
                successful_posts += 1
        
        return successful_posts


class SlackReferralsMessageView(SlackBaseView):
    
    def post(self, request):
        if bad_request := self.is_bad_request():
            return bad_request
        slack_poster = self.get_slack_poster(self.slack_cfg, self.data.get('is_test', True))
        error_msg = slack_poster.send_slack_job_post()
        if error_msg:
            return get_error_response(error_msg)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Slack message posted'
        })
    
    @staticmethod
    def get_slack_poster(slack_cfg, is_test):
        return SlackReferralPoster(
            slack_cfg, JobPost.PostChannel.SLACK_EMPLOYEE_REFERRAL.value,
            employer_id=slack_cfg.employer_id, is_test=is_test
        )
    
    @staticmethod
    def run_auto_posts():
        slack_cfgs = EmployerSlack.objects.select_related('employer').filter(
            is_enabled=True,
            referrals_post_channel__isnull=False
        )
        successful_posts = 0
        for slack_cfg in slack_cfgs:
            slack_poster = SlackReferralsMessageView.get_slack_poster(slack_cfg, False)
            error_msg = slack_poster.send_slack_job_post()
            if not error_msg:
                successful_posts += 1
        
        return successful_posts


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


class SlackExternalBaseView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [RawFormParser]
    
    def initial(self, request, *args, **kwargs):
        # Slack sends a test message periodically
        if not request.headers.get('X-Slack-Request-Timestamp'):
            logger.info(f'Slack test message sent to slash command URL: {request.data}')
            return Response(status=status.HTTP_200_OK)
        if not self.is_valid_slack_request(request):
            return Response(status=status.HTTP_403_FORBIDDEN, data='Invalid request signature')
        if payload := request.data.get('payload'):
            self.data = json.loads(payload)
            team_id = self.data['team']['id']
            team_domain = self.data['team']['domain']
            self.slack_user_id = self.data['user']['id']
        else:
            self.data = request.data
            team_id = self.data['team_id']
            team_domain = self.data['team_domain']
            self.slack_user_id = self.data['user_id']
        try:
            self.slack_cfg = EmployerSlack.objects.select_related('employer').get(team_key=team_id)
        except EmployerSlack.DoesNotExist:
            logger.error(f'Unknown Slack team key ({team_id}) for domain {team_domain}')
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Unknown team ID')
        self.slack_client = SlackBaseView.get_slack_client(token=self.slack_cfg.oauth_key)
        self.slack_user_profile = SlackBaseView.get_user_profile(self.slack_user_id, self.slack_client)
        
        super().initial(request, *args, **kwargs)
    
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


class SlackOptionsInboundView(SlackExternalBaseView):
    """Loads option data into a Slack select menu
    """
    
    def post(self, request):
        search_text = self.data['value']
        options = self.get_options(self.data['action_id'], search_text)
        options = self.add_new_option(options, search_text)
        return JsonResponse({"options": options}, status=status.HTTP_200_OK)
    
    @staticmethod
    def get_options(action_id, search_text):
        regex_pattern = f'^.*{search_text}.*$'
        if action_id == SelectEmployer.OPTIONS_LOAD_KEY:
            return [
                InputOption(employer.employer_name, employer.id).get_slack_object() for employer in
                Employer.objects.filter(Q(employer_name__iregex=regex_pattern))
            ]
        raise ValueError(f'Unknown option request for action ID = {action_id}')
    
    @staticmethod
    def add_new_option(options, search_text):
        for option in options:
            if option['text']['text'].lower() == search_text.lower():
                return options
        
        options.append(
            InputOption(f'{InputOption.NEW_VALUE_PREPEND}{search_text}', InputOption.NEW_VALUE_KEY).get_slack_object()
        )
        return options


class SlackWebhookInboundView(SlackExternalBaseView):
    
    def post(self, request):
        button_data = None
        if self.data['type'] == 'view_submission':
            action_id = self.data['view']['callback_id']
        elif self.data['type'] == 'block_actions':
            action_data = self.data['actions'][0]
            action_id = action_data['action_id']
            button_data = json.loads(self.data['actions'][0]['value'])
        else:
            raise ValueError('Unknown inbound type')
        
        if action_id == 'jv-referral':
            user = SlackBaseView.get_or_create_jobvyne_user(
                self.slack_user_profile,
                JobVyneUser.USER_TYPE_EMPLOYEE,
                self.slack_cfg,
                employer_id=self.slack_cfg.employer_id
            )
            job = EmployerJobView.get_employer_jobs(employer_job_id=button_data['job_id'])
            job_referral_link = SocialLink()
            job_referral_link = SocialLinkView.create_or_update_link(job_referral_link, {
                'owner_id': user.id,
                'employer_id': self.slack_cfg.employer_id,
                'job_ids': [job.id]
            })
            
            resp = self.slack_client.views_open(
                trigger_id=self.data['trigger_id'],
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
                                'text': '• You can copy this link and share it anywhere.\n• Anyone that applies using this link will be considered your referral.\n• You will be notified by email whenever you get a new referral.'
                            }
                        },
                    ],
                }
            )
        elif JobSeekerModalViews.is_modal_view(action_id):
            metadata = {}
            if raw_metadata := self.data['view']['private_metadata']:
                metadata = json.loads(raw_metadata)
            
            metadata = {**metadata, **Modal.get_modal_values(self.data)}
            
            # override slack user profile with user input values
            user = SlackBaseView.get_or_create_jobvyne_user(
                {**self.slack_user_profile, **metadata},
                JobVyneUser.USER_TYPE_CANDIDATE,
                self.slack_cfg
            )
            
            modal_views = JobSeekerModalViews(self.slack_user_profile, user, metadata)
            modal_view = modal_views.get_modal_view(callback_id=action_id, is_slack_object_only=False)
            if modal_view:
                modal_view.process_data(user)
                return Response(status=status.HTTP_200_OK, data={
                    'response_action': 'update',
                    'view': modal_view.get_slack_object()
                })
            else:
                confirmation_modal = modal_views.finalize_modal(
                    metadata,
                    user=user, slack_cfg=self.slack_cfg, slack_user_profile=self.slack_user_profile
                )
                return Response(status=status.HTTP_200_OK, data={
                    'response_action': 'update',
                    'view': confirmation_modal
                })
        elif JobModalViews.is_modal_view(action_id):
            metadata = {}
            if raw_metadata := self.data['view']['private_metadata']:
                metadata = json.loads(raw_metadata)
            
            metadata = {**metadata, **Modal.get_modal_values(self.data)}
            
            user = SlackBaseView.get_or_create_jobvyne_user(
                self.slack_user_profile, JobVyneUser.USER_TYPE_INFLUENCER, self.slack_cfg
            )
            modal_views = JobModalViews(self.slack_user_profile, user, metadata)
            modal_view = modal_views.get_modal_view(callback_id=action_id, is_slack_object_only=False)
            if modal_view:
                modal_view.process_data(user)
                return Response(status=status.HTTP_200_OK, data={
                    'response_action': 'update',
                    'view': modal_view.get_slack_object()
                })
            else:
                confirmation_modal = modal_views.finalize_modal(
                    metadata,
                    user=user, slack_cfg=self.slack_cfg, slack_user_profile=self.slack_user_profile
                )
                return Response(status=status.HTTP_200_OK, data={
                    'response_action': 'update',
                    'view': confirmation_modal
                })
        return Response(status=status.HTTP_200_OK)


class SlackCommandSuggestView(SlackExternalBaseView):
    
    def post(self, request):
        employer_suggestion = self.data['text']
        user_profile = SlackBaseView.get_user_profile(self.data['user_id'], self.slack_client)
        send_django_email(
            'New employer suggestion',
            'emails/base_general_email.html',
            to_email=[EMAIL_ADDRESS_SUPPORT],
            django_context={
                'is_exclude_final_message': True
            },
            html_body_content=f'<p>{user_profile["real_name"]} ({user_profile["email"]}) from {self.slack_cfg.employer.employer_name} recommended a new employer: {employer_suggestion}</p>',
            is_tracked=False,
            is_include_jobvyne_subject=False
        )
        return Response(status=status.HTTP_200_OK, data={
            'blocks': [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f':grapes: Thank you for the suggestion! Our support team will review and determine whether we can add {employer_suggestion}.'
                    }
                }
            ]
        })


class SlackCommandJobSeekerView(SlackExternalBaseView):
    
    def post(self, request):
        slack_user_profile = SlackBaseView.get_user_profile(self.data['user_id'], self.slack_client)
        user = SlackBaseView.get_or_create_jobvyne_user(
            self.slack_user_profile, JobVyneUser.USER_TYPE_CANDIDATE, self.slack_cfg
        )
        modal_views = JobSeekerModalViews(slack_user_profile, user, {'slack_user_id': self.slack_user_id})
        
        self.slack_client.views_open(
            view=modal_views.get_modal_view(modal_idx=0, is_next=False),
            trigger_id=self.data['trigger_id']
        )
        
        return Response(status=status.HTTP_200_OK)
    
    @staticmethod
    def send_job_slack_messages(current_dt, is_test=False):
        # Only send at 12:00 UTC
        if not (current_dt.hour == 12 and current_dt.minute == 0):
            return
        job_message_subscriptions = UserSocialSubscription.objects.select_related('user').filter(
            provider=OauthProviders.slack.value,
            subscription_type=UserSocialSubscription.SubscriptionType.jobs.value
        )
        slack_cfgs = {
            sc.id: sc for sc in EmployerSlack.objects.filter(
                id__in=[sub.subscription_data['slack_cfg_id'] for sub in job_message_subscriptions]
            )
        }
        
        successful_posts = 0
        for job_message_subscription in job_message_subscriptions:
            subscription_data = job_message_subscription.subscription_data
            slack_cfg = slack_cfgs[subscription_data['slack_cfg_id']]
            slack_poster = SlackJobRecipientPoster(
                slack_cfg, JobPost.PostChannel.SLACK_JOB.value,
                employer_id=slack_cfg.employer_id, recipient_id=subscription_data['user_id'], is_test=is_test,
                slack_user_id=subscription_data['slack_user_id'], message_data={'user': job_message_subscription.user}
            )
            error_msg = slack_poster.send_slack_job_post()
            if not error_msg:
                successful_posts += 1
        
        return successful_posts


class SlackCommandJobView(SlackExternalBaseView):
    
    def post(self, request):
        slack_user_profile = SlackBaseView.get_user_profile(self.data['user_id'], self.slack_client)
        user = SlackBaseView.get_or_create_jobvyne_user(
            self.slack_user_profile, JobVyneUser.USER_TYPE_INFLUENCER, self.slack_cfg
        )
        job_post_channel = None
        if self.slack_cfg.jobs_post_channel:
            job_post_channel = self.slack_client.conversations_info(channel=self.slack_cfg.jobs_post_channel)
        modal_views = JobModalViews(slack_user_profile, user, {
            'slack_user_id': self.slack_user_id,
            'post_channel_name': job_post_channel['channel']['name'] if job_post_channel else None,
            'group_name': self.slack_cfg.employer.employer_name,
            'group_id': self.slack_cfg.employer_id
        })
        
        self.slack_client.views_open(
            view=modal_views.get_modal_view(modal_idx=0, is_next=False),
            trigger_id=self.data['trigger_id']
        )
        
        return Response(status=status.HTTP_200_OK)
