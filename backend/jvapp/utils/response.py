import logging

import requests
from django.utils import timezone
from rest_framework.response import Response


logger = logging.getLogger(__name__)


def is_good_response(response, is_allow_300=False):
    max_code = 400 if is_allow_300 else 300
    return response.status_code >= 200 and response.status_code < max_code


def convert_resp_to_django_resp(resp: requests.Response) -> Response:
    return Response(
        data=resp.content,
        status=resp.status_code,
        content_type=resp.headers['Content-Type']
    )


class ProcessTimer:
    
    def __init__(self, process_name):
        self.process_name = process_name
        self.start_time = timezone.now()
        self.stop_time = None
        
    def stop(self):
        self.stop_time = timezone.now()
        
    def log_time(self, is_warning=False):
        if not self.stop_time:
            self.stop()
        process_time = (self.stop_time - self.start_time).total_seconds()
        log_type = logger.warning if is_warning else logger.info
        log_type(f'{self.process_name} process took {process_time} seconds to complete')
        