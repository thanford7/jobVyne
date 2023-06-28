import requests
from rest_framework.response import Response


def is_good_response(response, is_allow_300=False):
    max_code = 400 if is_allow_300 else 300
    return response.status_code >= 200 and response.status_code < max_code


def convert_resp_to_django_resp(resp: requests.Response) -> Response:
    return Response(
        data=resp.content,
        status=resp.status_code,
        content_type=resp.headers['Content-Type']
    )
