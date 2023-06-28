import hashlib
import hmac
import json
import logging
from typing import Union

from django.conf import settings
from django.db.models import F, Q
from django.db.transaction import atomic
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from slack_sdk import WebClient

from jobVyne.multiPartJsonParser import RawFormParser
from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY, get_error_response
from jvapp.apis.employer import EmployerJobView, EmployerSlackView
from jvapp.apis.social import SocialLinkPostJobsView, SocialLinkView
from jvapp.models.content import JobPost
from jvapp.models.employer import EmployerSlack
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
from jvapp.utils.slack_blocks import Modal
from jvapp.utils.slack_modals import JobSeekerModalViews

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
    def send_slack_job_post(self) -> Union[str, None]:
        """Return False if the post was successful"""
        if error_msg := self.has_error():
            return error_msg
        
        jobs = self.get_jobs_for_post()
        if not jobs and not self.is_test:
            msg = 'No new jobs to post to Slack'
            logger.info(msg)
            return msg
        
        if self.IS_PER_JOB_POST:
            for job in jobs:
                resp = self._send_slack_post(self.build_message(job, **self.message_data))
                raise_slack_exception_if_error(resp)
        else:
            resp = self._send_slack_post(self.build_message(jobs, **self.message_data))
            raise_slack_exception_if_error(resp)
        
        if not self.is_test:
            """
            Some employers create multiple posts for the same job with different locations
            We don't want to blast all of these posts - just send one of them.
            """
            jobs_filter = None
            for job in jobs:
                job_filter = Q(employer_id=job.employer_id, job_title=job.job_title)
                if not jobs_filter:
                    jobs_filter = job_filter
                else:
                    jobs_filter |= job_filter
            posted_jobs = EmployerJobView.get_employer_jobs(employer_job_filter=jobs_filter)
            
            job_posts = []
            for job in posted_jobs:
                job_posts.append(
                    JobPost(
                        employer_id=self.employer_id,
                        owner_id=self.owner_id,
                        recipient_id=self.recipient_id,
                        job_id=job.id,
                        channel=self.post_channel,
                        created_dt=timezone.now(),
                        modified_dt=timezone.now()
                    )
                )
            JobPost.objects.bulk_create(job_posts)
    
    def get_jobs_for_post(self):
        return SocialLinkPostJobsView.get_jobs_for_post(
            self.max_jobs, self.post_channel,
            employer_id=self.employer_id, owner_id=self.owner_id, recipient_id=self.recipient_id
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
            if job.employer.logo_square_88:
                job_info['accessory'] = {
                    'type': 'image',
                    'image_url': job.employer.logo_square_88.url,
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
    
        general_job_link = SocialLink.objects.get(employer_id=self.slack_cfg.employer.id, owner_id__isnull=True,
                                                  is_default=True)
        blocks.append({'type': 'divider'})
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
                    'text': ':grapes: JobVyne has a fresh batch of jobs ready to be plucked and enjoyed with a fresh glass of "get hired".'
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
        return resp['profile']
    
    @staticmethod
    def get_profile_picture(slack_user_profile):
        profile_picture_url = slack_user_profile.get('image_512')
        return convert_url_to_image(profile_picture_url, 'slack_profile_512.png')
    
    @staticmethod
    def get_or_create_jobvyne_user(slack_user_profile, user_type_bits, employer_id=None):
        try:
            user_filter = Q(email=slack_user_profile['email']) | Q(business_email=slack_user_profile['email'])
            user = JobVyneUser.objects.get(user_filter)
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
            for val, attr in (
                (linkedin_url, 'linkedin_url'),
                (first_name, 'first_name'),
                (last_name, 'last_name')
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
                JobVyneUser.USER_TYPE_CANDIDATE
            )
                
            modal_views = JobSeekerModalViews(self.slack_user_profile, user, metadata)
            modal_view = modal_views.get_modal_view_slack_object(callback_id=action_id)
            if modal_view:
                return Response(status=status.HTTP_200_OK, data={
                    'response_action': 'update',
                    'view': modal_view
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
            self.slack_user_profile, JobVyneUser.USER_TYPE_CANDIDATE
        )
        modal_views = JobSeekerModalViews(slack_user_profile, user, {'slack_user_id': self.slack_user_id})
        
        self.slack_client.views_open(
            view=modal_views.get_modal_view_slack_object(modal_idx=0, is_next=False),
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
