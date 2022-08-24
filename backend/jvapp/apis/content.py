from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models import SocialContentItem
from jvapp.models.abstract import PermissionTypes


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
