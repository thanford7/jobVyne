import logging

from rest_framework import status

from jvapp.apis._apiBase import JobVyneAPIView
from .pull import pull_events

logger = logging.getLogger(__name__)

from rest_framework.response import Response

class EventPullView(JobVyneAPIView):
    def post(self, request):
        limit = self.data.get('limit')
        pull_events(limit)
        return Response(status=status.HTTP_200_OK)
