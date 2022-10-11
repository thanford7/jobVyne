from django.core.files import File
from django.http import QueryDict
from rest_framework.views import APIView


SUCCESS_MESSAGE_KEY = 'successMessage'
WARNING_MESSAGES_KEY = 'warningMessages'
ERROR_MESSAGES_KEY = 'errorMessages'


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
        super().initial(request, *args, **kwargs)
