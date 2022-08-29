from django.core.files.base import ContentFile
from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.models import EmployerFile, SocialContentItem, SocialPost, SocialPostFile, UserFile
from jvapp.models.abstract import PermissionTypes
from jvapp.serializers.content import get_serialized_social_post
from jvapp.utils.data import set_object_attributes


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
    
        posts = SocialPost.objects.filter(filter)
        posts = SocialPost.jv_filter_perm(self.user, posts)
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
        # TODO: Post to social sites if user has specified
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Post created'
        })
    
    @atomic
    def put(self, request, post_id):
        pass
    
    @atomic
    def delete(self, request, post_id):
        pass
    
    @staticmethod
    @atomic
    def update_social_post(user, post, data):
        set_object_attributes(post, data, {
            'content': None,
            'formattedContent': None
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
                file=ContentFile(file.read())
            ).save()
        
        return post