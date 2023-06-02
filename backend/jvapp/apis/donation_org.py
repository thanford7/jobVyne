import json

import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, get_error_response

EVERY_ORG_URL = 'https://partners.every.org/v0.2/'


class DonationOrgSearchView(JobVyneAPIView):
    MAX_RESULTS = 10
    
    def get(self, request):
        if not (search_text := self.query_params.get('search_text')):
            return Response(status=status.HTTP_200_OK, data=[])
        
        organizations = self.get_raw_donation_orgs(search_text)
        return Response(status=status.HTTP_200_OK, data=organizations)
    
    @staticmethod
    def get_raw_donation_orgs(search_text):
        # https://docs.every.org/docs/endpoints/nonprofit-search
        
        # Request by organization name
        search_resp = requests.get(
            f'{EVERY_ORG_URL}search/{search_text}',
            params={'apiKey': settings.EVERY_ORG_PUBLIC_KEY, 'take': DonationOrgSearchView.MAX_RESULTS}
        )
        search_results = json.loads(search_resp.content)
        
        # Request by organization type
        browse_resp = requests.get(
            f'{EVERY_ORG_URL}browse/{search_text}',
            params={'apiKey': settings.EVERY_ORG_PUBLIC_KEY, 'take': DonationOrgSearchView.MAX_RESULTS}
        )
        browse_results = json.loads(browse_resp.content)
        
        return search_results['nonprofits'] + browse_results['nonprofits']
    
    
class DonationOrgView(JobVyneAPIView):
    
    def get(self, request):
        if not (ein := self.query_params.get('ein')):
            return get_error_response('An EIN is required')
    
        organization = self.get_raw_donation_org(ein)
        return Response(status=status.HTTP_200_OK, data=organization)
    
    @staticmethod
    def get_raw_donation_org(ein):
        resp = requests.get(
            f'{EVERY_ORG_URL}nonprofit/{ein}',
            params={'apiKey': settings.EVERY_ORG_PUBLIC_KEY}
        )
        org = json.loads(resp.content)
        return org['data']['nonprofit']
