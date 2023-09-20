import json

from django.contrib.auth.models import AnonymousUser
from django.core.files import File
from django.http import QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


SUCCESS_MESSAGE_KEY = 'successMessage'
WARNING_MESSAGES_KEY = 'warningMessages'
ERROR_MESSAGES_KEY = 'errorMessages'
REDIRECT_KEY = 'REDIRECT'


def get_redirect_response(redirect_url):
    return Response(status=status.HTTP_200_OK, data={
        REDIRECT_KEY: redirect_url
    })


def get_error_response(error_message):
    return Response(status=status.HTTP_200_OK, data={
        ERROR_MESSAGES_KEY: [error_message]
    })


def get_warning_response(warning_message):
    return Response(status=status.HTTP_200_OK, data={
        WARNING_MESSAGES_KEY: [warning_message]
    })


def get_success_response(success_message):
    return Response(status=status.HTTP_200_OK, data={
        SUCCESS_MESSAGE_KEY: success_message
    })


def get_files(request):
    if not request.data:
        return None

    files = {}
    for key, val in request.data.items():
        if isinstance(val, File):
            files[key] = request.data.getlist(key)

    return files


class JobVyneAPIView(APIView):
    
    def initial(self, request, *args, **kwargs):
        self.data = request.data.dict() if isinstance(request.data, QueryDict) else request.data
        self.query_params = request.query_params
        # Django's dict method doesn't work for files - it drops all but the first uploaded file
        self.files = get_files(request)
        self.user = request.user
        if isinstance(self.user, AnonymousUser):
            self.user = None
        super().initial(request, *args, **kwargs)
        
    def get_query_param_list(self, key, default=None):
        val = self.query_params.get(key, default)
        if isinstance(val, str):
            val = json.loads(val)
        if not isinstance(val, list):
            val = [val]
        return val
