from django.db.models import Q
from rest_framework import status, authentication
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models.user import JobVyneUser
from jvapp.serializers.user import get_serialized_user


class UserView(JobVyneAPIView):
    authentication_classes = [authentication.SessionAuthentication]

    def get(self, request, user_id=None):
        data = request.data
        if user_id:
            user = JobVyneUser.objects.get(id=user_id)
            return Response(status=status.HTTP_200_OK, data=get_serialized_user(user))
        elif searchText := data.get('search'):
            searchText = searchText[0]
            userFilter = Q(firstName__iregex=f'^.*{searchText}.*$')
            userFilter |= Q(lastName__iregex=f'^.*{searchText}.*$')
            userFilter |= Q(email__iregex=f'^.*{searchText}.*$')
            users = JobVyneUser.objects.filter(userFilter)
            return Response(status=status.HTTP_200_OK, data=[get_serialized_user(u) for u in users])

        return Response('Please provide a user ID or search text', status=status.HTTP_400_BAD_REQUEST)