import logging

from rest_framework import status

from jvapp.apis._apiBase import JobVyneAPIView
from .summarize import pull_articles

logger = logging.getLogger(__name__)

from rest_framework.response import Response

class ArticleSummarizeView(JobVyneAPIView):
    def post(self, request):
        limit = self.data.get('limit')
        pull_articles(limit)
        return Response(status=status.HTTP_200_OK)
