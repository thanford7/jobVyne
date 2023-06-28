import os
import openai
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

openai.api_key = os.getenv('OPEN_AI_API_KEY')
COMPANY_SEARCH_COUNT = 10

class JobSearchView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # TODO: WIP - the idea is to allow users to search for companies that fit specific parameters
        start_msg = f'Give me a list of {COMPANY_SEARCH_COUNT} companies with the following characteristics'
        end_msg = 'in the format <company name>:<website>'
        resp = openai.Completion.create(
            model='text-babbage-001',
            prompt='Say this is a test',
            max_tokens=500,
            temperature=0.8
        )
        return Response(status=status.HTTP_200_OK)
