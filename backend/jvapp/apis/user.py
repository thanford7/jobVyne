from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models.user import JobVyneUser
from jvapp.serializers.user import get_serialized_user


class UserView(JobVyneAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, user_id=None):
        # This allows use to check authentication and conditionally grab user info in one request
        if not all((request.user, request.user.is_authenticated)):
            return Response(status=status.HTTP_200_OK, data=False)
        data = request.data
        if user_id:
            user = self.get_user(user_id=user_id)
            return Response(status=status.HTTP_200_OK, data=get_serialized_user(user))
        elif search_text := data.get('search'):
            search_text = search_text[0]
            user_filter = Q(firstName__iregex=f'^.*{search_text}.*$')
            user_filter |= Q(lastName__iregex=f'^.*{search_text}.*$')
            user_filter |= Q(email__iregex=f'^.*{search_text}.*$')
            users = self.get_user(user_filter=user_filter)
            return Response(status=status.HTTP_200_OK, data=[get_serialized_user(u) for u in users])

        return Response('Please provide a user ID or search text', status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_user(user_id=None, user_filter=None):
        if user_id:
            user_filter = Q(id=user_id)
    
        users = JobVyneUser.objects.prefetch_related('application_template').filter(user_filter)
    
        if user_id:
            if not users:
                raise JobVyneUser.DoesNotExist
            return users[0]
    
        return users
