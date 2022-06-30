from django.db.models import Q
from rest_framework import status, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from jvapp.models.user import *
from jvapp.serializers.user import get_serialized_user


class UserView(APIView):
    authentication_classes = [authentication.SessionAuthentication]

    def get(self, request, userId=None):
        data = request.data
        if userId:
            user = JobVineUser.objects.get(id=userId)
            return Response(status=status.HTTP_200_OK, data=get_serialized_user(user))
        elif searchText := data.get('search'):
            searchText = searchText[0]
            userFilter = Q(firstName__iregex=f'^.*{searchText}.*$')
            userFilter |= Q(lastName__iregex=f'^.*{searchText}.*$')
            userFilter |= Q(email__iregex=f'^.*{searchText}.*$')
            users = JobVineUser.objects.filter(userFilter)
            return Response(status=status.HTTP_200_OK, data=[get_serialized_user(u) for u in users])

        return Response('Please provide a user ID or search text', status=status.HTTP_400_BAD_REQUEST)