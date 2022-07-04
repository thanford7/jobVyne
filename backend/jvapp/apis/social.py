from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models import SocialPlatform
from jvapp.serializers.social import get_serialized_social_platform


class SocialPlatformView(JobVyneAPIView):
    
    def get(self, request):
        data = [get_serialized_social_platform(sp) for sp in SocialPlatform.objects.all()]
        return Response(status=status.HTTP_200_OK, data=data)
