import json
import re

import requests
from django.db.models import Q
from django.db.transaction import atomic
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import ERROR_MESSAGES_KEY, JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.models import EmployerFile, SocialContentItem, SocialPost, SocialPostAudit, SocialPostFile, UserFile
from jvapp.models.abstract import PermissionTypes
from jvapp.models.user import UserSocialCredential
from jvapp.serializers.content import get_serialized_social_post
from jvapp.utils.data import set_object_attributes
from jvapp.utils.oauth import OAUTH_CFGS


def _get_url(text):
    url_match = re.search('https://\S+', text, re.IGNORECASE)
    return url_match.group(0) if url_match else None


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
        
        item = SocialContentItem(
            employer_id=employer_id,
            user_id=user_id,
            content=self.data['content']
        )
        item.jv_check_permission(PermissionTypes.CREATE.value, self.user)
        item.save()
        return Response(status=status.HTTP_200_OK)
    
    @atomic
    def delete(self, request, item_id):
        item = SocialContentItem.objects.get(id=item_id)
        item.jv_check_permission(PermissionTypes.DELETE.value, self.user)
        item.delete()
        return Response(status=status.HTTP_200_OK)


class SocialPostView(JobVyneAPIView):
    
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
        
        posts = self.get_social_posts(self.user, filter=filter)
        return Response(status=status.HTTP_200_OK, data=[get_serialized_social_post(post) for post in posts])
    
    @atomic
    def post(self, request):
        employer_id = self.data.get('employer_id')
        user_id = self.data.get('user_id')
        if not any([employer_id, user_id]):
            return Response('An employer ID or user ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        post = SocialPost(
            employer_id=employer_id,
            user_id=user_id
        )
        self.update_social_post(self.user, post, self.data)
        ShareSocialPostView.post_to_accounts(self.user, post.id, self.data['post_accounts'])
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
            'formatted_content': None
        })
        
        permission_type = PermissionTypes.EDIT.value if post.id else PermissionTypes.CREATE.value
        post.jv_check_permission(permission_type, user)
        post.save()
        
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
            .select_related('user', 'employer') \
            .prefetch_related('file', 'audit') \
            .filter(filter)
        posts = SocialPost.jv_filter_perm(user, posts)
        if post_id:
            if not posts:
                raise SocialPost.DoesNotExist
            return posts[0]
        
        return posts


class ShareSocialPostView(JobVyneAPIView):
    
    def post(self, request):
        if not (post_id := self.data.get('post_id')):
            return Response('A post ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        errors = self.post_to_accounts(self.user, post_id, self.data['post_accounts'])
        data = {}
        if errors:
            data[ERROR_MESSAGES_KEY] = errors
        
        return Response(status=status.HTTP_200_OK, data=data)
        
    @staticmethod
    def post_to_accounts(user, post_id, post_accounts):
        post = SocialPostView.get_social_posts(user, post_id=post_id)
        file = next((f for f in post.file.all()), None)
        social_credentials = {
            (cred.provider, cred.email): cred for cred in UserSocialCredential.objects.filter(user_id=user.id)
        }
    
        errors = []
        for post_account in post_accounts:
            cred = social_credentials.get((post_account['provider'], post_account['email']))
            if not cred:
                errors.append(
                    f'No account credentials were found for {post_account["platform_name"]} with email {post_account["email"]}')
                continue
        
            args = [cred.access_token, post.formatted_content]
            kwargs = {'post_file': file.file if file else None}
            resp = None
            if cred.provider == 'linkedin-oauth2':
                resp = ShareSocialPostView.post_to_linkedin(*args, **kwargs)
            
            status = None if not resp else resp.get('status')
            if status and (status >= 300 or status < 200):
                errorText = f'Issue with post to {post_account["platform_name"]} with email {post_account["email"]}. {resp["status"]}: '
                if msg := resp.get('message'):
                    errorText += msg
                errors.append(errorText)
            elif resp:
                SocialPostAudit(
                    social_post=post,
                    email=cred.email,
                    platform=OAUTH_CFGS[cred.provider]['name'],
                    posted_dt=timezone.now()
                ).save()
        
        return errors
    
    @staticmethod
    def post_to_linkedin(access_token, post_content, post_file=None):
        authorization_header = {'Authorization': f'Bearer {access_token}'}
        authorization_param = {'oauth2_access_token': access_token}
        profile_response = requests.get(
            url='https://api.linkedin.com/v2/me',
            headers=authorization_header
        )
        profile = profile_response.json()
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
