import base64
import json
import re

import requests
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models import EmployerAts
from jvapp.models.abstract import PermissionTypes
from jvapp.permissions.employer import IsAdminOrEmployerPermission
from jvapp.utils.response import convert_resp_to_django_resp, is_good_response


class GreenhouseAts:
    jobs_url = 'https://harvest.greenhouse.io/v1/job_posts'
    
    @classmethod
    def get_jobs(cls, ats_cfg):
        headers = cls.get_request_headers(ats_cfg)
        data = []
        has_next_page = True
        page = 1
        while has_next_page:
            resp = requests.get(
                cls.jobs_url,
                headers=headers,
                params={
                    'per_page': 500,
                    'page': page,
                    'active': True,
                    'full_content': True
                }
            )
            if not is_good_response(resp):
                return resp
            data += cls.get_resp_data(resp)
            has_next_page = cls.has_next_page(resp, page)
            page += 1
        return data
    
    @classmethod
    def save_jobs(cls, jobs):
        pass
    
    @classmethod
    def get_request_headers(cls, ats_cfg):
        encoded_api_key_b = base64.b64encode(f'{ats_cfg.api_key}:'.encode())  # Must be in bytes to encode
        encoded_api_key = str(encoded_api_key_b, encoding='utf-8')  # Convert back to string val so it can be concattenated
        return {
            # 'On-Behalf-Of': ats_cfg.email,
            'Authorization': f'Basic {encoded_api_key}'
        }
    
    @classmethod
    def get_resp_data(cls, resp):
        return json.loads(resp.text)
    
    @classmethod
    def has_next_page(cls, resp, page):
        if not hasattr(resp, 'links'):
            return False
        last_page_match = re.match('^.*?page=(?P<page>[0-9]+).*?$', resp.links['last']['url'])
        last_page = int(last_page_match.group('page'))
        return page < last_page


ats_map = {
    'greenhouse': GreenhouseAts
}


class AtsJobsView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    
    def put(self, request):
        if not (ats_id := self.data.get('ats_id')):
            return Response('An ATS ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        ats_cfg = EmployerAts.objects.get(id=ats_id)
        ats_cfg.jv_check_permission(PermissionTypes.EDIT.value, self.user)
        ats_api = ats_map[ats_cfg.name]
        jobs = ats_api.get_jobs(ats_cfg)
        
        # If we get a response back, something has gone wrong
        if isinstance(jobs, requests.Response):
            return convert_resp_to_django_resp(jobs)
        
        return Response(status=status.HTTP_200_OK, data=jobs)
