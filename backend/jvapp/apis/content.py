import json
import re

import requests
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import ExtractHour, ExtractIsoWeekDay, ExtractMinute
from django.db.transaction import atomic
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import ERROR_MESSAGES_KEY, JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.apis.auth import get_refreshed_access_token
from jvapp.apis.social import SocialLinkJobsView, SocialLinkPostJobsView, SocialLinkView
from jvapp.models.abstract import PermissionTypes
from jvapp.models.content import JobPost, SocialContentItem, SocialPost, SocialPostAudit, SocialPostFile
from jvapp.models.employer import EmployerFile
from jvapp.models.user import UserFile
from jvapp.serializers.content import get_serialized_social_post
from jvapp.utils.data import AttributeCfg, set_object_attributes
from jvapp.utils.datetime import get_datetime_or_none
from jvapp.utils.email import ContentPlaceholders
from jvapp.utils.oauth import OAUTH_CFGS, OauthProviders


def _get_url(text):
    url_match = re.search('https://\S+', text, re.IGNORECASE)
    return url_match.group(0) if url_match else None


MAX_JOBS_TO_POST = 10


class SocialContentItemView(JobVyneAPIView):
    
    def get(self, request):
        employer_id = self.query_params.get('employer_id')
        user_id = self.query_params.get('user_id')
        if not any([employer_id, user_id]):
            return Response('An employer ID or user ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        filters = []
        if employer_id:
            filters.append(Q(employer_id=employer_id))
        if user_id:
            filters.append(Q(user_id=user_id))
        filter = None
        for f in filters:
            if not filter:
                filter = f
            else:
                filter |= f
        
        items = SocialContentItem.objects.filter(filter)
        items = SocialContentItem.jv_filter_perm(self.user, items)
        return Response(status=status.HTTP_200_OK, data=[
            {
                'id': item.id,
                'employer_id': item.employer_id,
                'user_id': item.user_id,
                'content': item.content
            } for item in items
        ])
    
    @atomic
    def put(self, request):
        item = SocialContentItem.objects.get(id=self.data['id'])
        item.content = self.data['content']
        item.jv_check_permission(PermissionTypes.EDIT.value, self.user)
        item.save()
        return Response(status=status.HTTP_200_OK)
    
    @atomic
    def post(self, request):
        employer_id = self.data.get('employer_id')
        user_id = self.data.get('user_id')
        if not any([employer_id, user_id]):
            return Response('An employer ID or user ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        self.create_social_content_item(employer_id, user_id, self.data['content'], self.user)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Successfully created new template'
        })
    
    @atomic
    def delete(self, request, item_id):
        item = SocialContentItem.objects.get(id=item_id)
        item.jv_check_permission(PermissionTypes.DELETE.value, self.user)
        item.delete()
        return Response(status=status.HTTP_200_OK)
    
    @staticmethod
    def create_social_content_item(employer_id, user_id, content, user):
        filter = Q(employer_id=employer_id) | Q(user_id=user_id)
        current_content = {ci.content for ci in SocialContentItem.objects.filter(filter)}
        if content in current_content:
            return
        
        item = SocialContentItem(
            employer_id=employer_id,
            user_id=user_id,
            content=content
        )
        item.jv_check_permission(PermissionTypes.CREATE.value, user)
        item.save()
        return item


class SocialPostView(JobVyneAPIView):
    
    def get(self, request):
        employer_id = self.query_params.get('employer_id')
        user_id = self.query_params.get('user_id')
        is_employees = self.query_params.get('is_employees')
        if not any([employer_id, user_id]):
            return Response('An employer ID or user ID is required', status=status.HTTP_400_BAD_REQUEST)
        if is_employees and not employer_id:
            return Response('An employer ID is required to fetch employee posts', status=status.HTTP_400_BAD_REQUEST)
        
        page_count = self.query_params.get('page_count', 1)
        
        filters = []
        if employer_id and is_employees:
            filters.append(Q(user__employer_id=employer_id))
        elif employer_id:
            filters.append(Q(employer_id=employer_id))
        if user_id:
            filters.append(Q(user_id=user_id))
        filter = None
        for f in filters:
            if not filter:
                filter = f
            else:
                filter |= f
                
        if filter_params := self.query_params.get('filter_params'):
            filter_params = json.loads(filter_params)
            add_filters = Q()
            if start_date := filter_params.get('start_date'):
                add_filters &= Q(created_dt__gte=get_datetime_or_none(start_date))
            if end_date := filter_params.get('end_date'):
                add_filters &= Q(created_dt__lte=get_datetime_or_none(end_date))
            if employee_ids := filter_params.get('employee_ids'):
                add_filters &= Q(user_id__in=employee_ids)
            filter &= add_filters
        
        posts = self.get_social_posts(self.user, filter=filter)
        paged_posts = Paginator(posts, per_page=8)
        return Response(status=status.HTTP_200_OK, data={
            'total_page_count': paged_posts.num_pages,
            'posts': [get_serialized_social_post(post) for post in paged_posts.get_page(page_count)]
        })
    
    @atomic
    def put(self, request):
        post_id = self.data.get('post_id')
        employer_id = self.data.get('employer_id')
        user_id = self.data.get('user_id')
        if not any([employer_id, user_id]):
            return Response('An employer ID or user ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        if post_id:
            post = self.get_social_posts(self.user, post_id=post_id)
        else:
            post = SocialPost(
                employer_id=employer_id,
                user_id=user_id
            )
        post = self.update_social_post(self.user, post, self.data)
        SocialContentItemView.create_social_content_item(employer_id, user_id, self.data['content'], self.user)
        if self.data.get('is_post_now'):
            ShareSocialPostView.post_to_accounts(post)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Post created'
        })
    
    @atomic
    def delete(self, request, post_id):
        post = SocialPost.objects.get(id=post_id)
        post.jv_check_permission(PermissionTypes.DELETE.value, self.user)
        post.delete()
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Post deleted'
        })
    
    @staticmethod
    @atomic
    def update_social_post(user, post, data):
        set_object_attributes(post, data, {
            'content': None,
            'is_auto_post': None,
            'auto_weeks_between': None,
            'auto_start_dt': None,
            'auto_day_of_week': None,
            'social_link_id': None
        })
        
        permission_type = PermissionTypes.EDIT.value if post.id else PermissionTypes.CREATE.value
        post.jv_check_permission(permission_type, user)
        post.save()

        # Clear any credentials for social accounts and add the new ones
        post.post_credentials.set(data.get('post_account_ids', []))
        
        file = None
        if employer_file_id := data.get('employer_file_id'):
            file = EmployerFile.objects.get(id=employer_file_id)
            # No need to check permission because employer files are meant to be shared with employees and others
        if user_file_id := data.get('user_file_id'):
            file = UserFile.objects.get(id=user_file_id)
            file.jv_check_permission(PermissionTypes.CREATE.value, user)  # Make sure the user owns this file
        
        SocialPostFile.objects.filter(social_post_id=post.id).delete()
        if file:
            SocialPostFile(
                social_post=post,
                file=file.file
            ).save()
        
        return post
    
    @staticmethod
    def get_social_posts(user, post_id=None, filter=None):
        filter = filter or Q()
        if post_id:
            filter = Q(id=post_id)
        
        posts = SocialPost.objects \
            .select_related('user', 'employer', 'social_link', 'social_link__employer') \
            .prefetch_related('file', 'audit', 'child_post', 'post_credentials') \
            .filter(filter)
        posts = SocialPost.jv_filter_perm(user, posts)
        if post_id:
            if not posts:
                raise SocialPost.DoesNotExist
            return posts[0]
        
        return posts
    
    @staticmethod
    def get_formatted_content(post, jobs, platform_name):
        formatted_content = ''
        if not post.content:
            return formatted_content
        
        formatted_content = post.content.replace(
            ContentPlaceholders.EMPLOYER_NAME.value,
            post.social_link.employer.employer_name if post.social_link.employer else ''
        )
        
        job_link = post.social_link.get_link_url()
        formatted_content = formatted_content.replace(
            ContentPlaceholders.JOB_LINK.value,
            job_link
        )
        
        jobs_list = '\n\n'.join([(
                f'🏢 Employer: {job.employer.employer_name}\n'
                f'💼 Job: {job.job_title}\n'
                f'📍 Locations: {job.locations_text}\n'
                f'💰 Salary: {job.salary_text}\n'
                f'🔗 Apply: {SocialLinkView.get_or_create_single_job_link(job, owner_id=post.user_id, employer_id=post.employer_id).get_link_url(platform_name=platform_name)}'
            ) for job in jobs
        ])

        formatted_content = formatted_content.replace(
            ContentPlaceholders.JOBS_LIST.value,
            jobs_list
        )
        return formatted_content


class ShareSocialPostView(JobVyneAPIView):
    
    def post(self, request):
        if not (post_id := self.data.get('post_id')):
            return Response('A post ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        post, is_new = self.create_or_update_post(self.user, post_id, self.data)
        data = {}
        if self.data.get('is_post_now'):
            errors, _ = self.post_to_accounts(post)
            if errors:
                data[ERROR_MESSAGES_KEY] = errors
            else:
                data[SUCCESS_MESSAGE_KEY] = 'Successfully posted'
        else:
            data[SUCCESS_MESSAGE_KEY] = 'Created post' if is_new else 'Updated post'
            
        return Response(status=status.HTTP_200_OK, data=data)
    
    @staticmethod
    def update_common_post_attributes(post, data):
        set_object_attributes(post, data, {
            'is_auto_post': None,
            'auto_weeks_between': None,
            'auto_start_dt': None,
            'auto_day_of_week': None,
            'social_link_id': None
        })
    
    @staticmethod
    @atomic
    def create_or_update_post(user, post_id, data):
        post = SocialPostView.get_social_posts(user, post_id=post_id)
        owner_id = data.get('owner_id')
    
        # Copy a post template that an employer created and assign it to the user that is posting
        is_new = bool(owner_id)
        if is_new:
            new_post = SocialPost(
                user_id=owner_id,
                content=post.content,
                original_post=post  # Allows us to track how many employees shared an employer's post
            )
            ShareSocialPostView.update_common_post_attributes(new_post, data)
            new_post.jv_check_permission(PermissionTypes.CREATE.value, user)
            new_post.save()
            for file in post.file.all():
                SocialPostFile(
                    social_post=new_post,
                    file=file.file
                ).save()
        
            post = new_post
        else:
            # Update to the most recent content to account for changes in open jobs
            ShareSocialPostView.update_common_post_attributes(post, data)
            post.save()
        
        # Clear any credentials for social accounts and add the new ones
        post.post_credentials.clear()
        for cred_id in data['post_account_ids']:
            post.post_credentials.add(cred_id)
        
        # Refetch to efficiently grab related objects for later use
        return SocialPost.objects.prefetch_related('file', 'post_credentials').get(id=post.id), is_new
        
    @staticmethod
    def post_to_accounts(post, is_catch_errors=False):
        errors = []
        successful_posts = 0
        file = next((f for f in post.file.all()), None)
        post_accounts = ShareSocialPostView.get_post_accounts(post)
    
        for post_account in post_accounts:
            post_account_credential = post_account['credential']
            platform_name = OAUTH_CFGS[post_account_credential.provider]['name']
            formatted_content = SocialPostView.get_formatted_content(post, post_account['jobs'], platform_name)
            args = [post.user, post_account_credential.access_token, formatted_content]
            kwargs = {'post_file': file.file if file else None}
            resp = None
            if post_account_credential.provider == 'linkedin-oauth2':
                if is_catch_errors:
                    try:
                        resp = ShareSocialPostView.post_to_linkedin(*args, **kwargs)
                    # We want to be very permissive to make sure an issue with one account doesn't prevent other posts to go out
                    except:
                        errors.append(f'(User ID = ${post.user_id}) Issue with post to {platform_name} with email {post_account_credential.email}')
                        continue
                else:
                    resp = ShareSocialPostView.post_to_linkedin(*args, **kwargs)
            
            status = None if not resp else resp.get('status')
            if status and (status >= 300 or status < 200):
                errorText = f'(User ID = ${post.user_id}) Issue with post to {platform_name} with email {post_account_credential.email}. {resp["status"]}: '
                if msg := resp.get('message'):
                    errorText += msg
                errors.append(errorText)
            elif resp:
                SocialPostAudit(
                    social_post=post,
                    formatted_content=formatted_content,
                    email=post_account_credential.email,
                    platform=platform_name,
                    posted_dt=timezone.now()
                ).save()
                successful_posts += 1
        
        return errors, successful_posts
    
    @staticmethod
    def is_auto_post_week(post, target_dt):
        # TODO: Add django tests for this method
        week_diff = (target_dt.date() - post.auto_start_dt.date()).days / 7
        return (week_diff % post.auto_weeks_between) == 0
    
    @staticmethod
    def run_auto_posts(target_dt):
        if not settings.IS_SEND_AUTO_POSTS:
            return ['Auto-posts have been disabled in the configuration settings'], 0
        
        auto_posts = SocialPost.objects\
            .select_related(
                'social_link'
            ) \
            .prefetch_related(
                'file',
                'post_credentials',
                'social_link__job_subscriptions',
                'social_link__job_subscriptions__filter_job',
                'social_link__job_subscriptions__filter_employer',
                'social_link__job_subscriptions__filter_location',
                'social_link__job_subscriptions__filter_location__city',
                'social_link__job_subscriptions__filter_location__state',
                'social_link__job_subscriptions__filter_location__country',
            ) \
            .annotate(auto_post_minute=ExtractMinute('auto_start_dt')) \
            .annotate(auto_post_hour=ExtractHour('auto_start_dt')) \
            .annotate(auto_post_dow=ExtractIsoWeekDay('auto_start_dt') - 1) \
            .filter(
                is_auto_post=True,
                social_link__isnull=False,
                auto_post_dow=target_dt.weekday(),
                auto_post_minute=target_dt.minute,
                auto_post_hour=target_dt.hour,
                auto_start_dt__lte=target_dt
            )
        
        auto_posts = [ap for ap in auto_posts if ShareSocialPostView.is_auto_post_week(ap, target_dt)]
        
        # Send the post
        errors = []
        successful_posts = 0
        for post in auto_posts:
            new_errors, new_successful_posts = ShareSocialPostView.post_to_accounts(post, is_catch_errors=True)
            errors += new_errors
            successful_posts += new_successful_posts
        
        return errors, successful_posts
    
    @staticmethod
    def get_post_accounts(post):
        post_accounts = [
            {
                'credential': post_cred,
                'jobs': SocialLinkPostJobsView.get_jobs_for_post(
                    MAX_JOBS_TO_POST,
                    ShareSocialPostView.get_post_channel_by_provider(post_cred.provider),
                    user_id=post.user_id,
                    employer_id=post.employer_id,
                    job_subscriptions=post.social_link.job_subscriptions.all()
                )
            } for post_cred in post.post_credentials.all()
        ]
    
        # Filter out post accounts with no available jobs
        return [pa for pa in post_accounts if pa['jobs']]
    
    @staticmethod
    def get_linkedin_profile(access_token):
        authorization_header = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(
            url='https://api.linkedin.com/v2/me',
            headers=authorization_header
        )
        return profile_response.json()
    
    @staticmethod
    def post_to_linkedin(user, access_token, post_content, post_file=None):
        profile = ShareSocialPostView.get_linkedin_profile(access_token)
        if serviceErrorCode := profile.get('serviceErrorCode'):
            if serviceErrorCode == 65602:  # Token has expired. Try refreshing token
                access_token = get_refreshed_access_token(OauthProviders.linkedin.value, user)
                profile = ShareSocialPostView.get_linkedin_profile(access_token)
                if serviceErrorCode := profile.get('serviceErrorCode'):
                    raise ConnectionError(f'{serviceErrorCode}: {profile.get("message")}')
            else:
                raise ConnectionError(f'{serviceErrorCode}: {profile.get("message")}')
        author_urn = f'urn:li:person:{profile["id"]}'
    
        data = {
            'author': author_urn,
            'lifecycleState': 'PUBLISHED',
            'specificContent': {
                'com.linkedin.ugc.ShareContent': {
                    'shareCommentary': {
                        'text': post_content
                    },
                    'shareMediaCategory': 'NONE'
                }
            },
            'visibility': {
                'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
            }
        }

        authorization_param = {'oauth2_access_token': access_token}
        if post_file:
            # https://docs.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin?context=linkedin%2Fconsumer%2Fcontext
            # Step 1: Register the image upload
            register_response = requests.post(
                url='https://api.linkedin.com/v2/assets?action=registerUpload',
                params=authorization_param,
                data=json.dumps({
                    'registerUploadRequest': {
                        'recipes': [
                            'urn:li:digitalmediaRecipe:feedshare-image'
                        ],
                        'owner': author_urn,
                        'serviceRelationships': [
                            {
                                'relationshipType': 'OWNER',
                                'identifier': 'urn:li:userGeneratedContent'
                            }
                        ]
                    }
                })
            )
            register_response_data = register_response.json()
            image_url = register_response_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            
            # Step 2: Upload image
            resp = requests.post(
                url=image_url,
                params=authorization_param,
                data=post_file.open().read()
            )
            post_file.close()
            
            if resp.status_code >= 300 or resp.status_code < 200:
                raise ValueError(f'Unable to upload image: {resp.reason}')
            
            # Step 3: Add the image asset to the post
            data['specificContent']['com.linkedin.ugc.ShareContent']['shareMediaCategory'] = 'IMAGE'
            data['specificContent']['com.linkedin.ugc.ShareContent']['media'] = [
                {
                    'status': 'READY',
                    'media': register_response_data['value']['asset']
                }
            ]
        elif url := _get_url(post_content):
            data['specificContent']['com.linkedin.ugc.ShareContent']['shareMediaCategory'] = 'ARTICLE'
            data['specificContent']['com.linkedin.ugc.ShareContent']['media'] = [
                {
                    'status': 'READY',
                    'originalUrl': url,
                }
            ]
        
        post_response = requests.post(
            url='https://api.linkedin.com/v2/ugcPosts',
            headers={'X-Restli-Protocol-Version': '2.0.0'},
            params=authorization_param,
            data=json.dumps(data)
        )
        
        return post_response.json()

    @staticmethod
    def get_post_channel_by_provider(provider_name):
        if provider_name == OauthProviders.linkedin.value:
            return JobPost.PostChannel.LINKEDIN_JOB.value
        # Note: Will add more as we build more integrations
        return None
