import logging
import re

from django.conf import settings
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


class AdminRedirectMiddleware:
    """
    The DigitalOcean backend is routed through 'backend/...', but the 'backend'
    part of the URL is dropped. When using the Django admin on the live site,
    it is necessary to add the 'backend' portion of the URL back in for proper routing
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if (not settings.IS_LOCAL) and re.match('/django-admin/.*', request.path) and response.status_code == 404:
            response = redirect(f'/backend{request.path}')

        return response


class ErrorHandlerMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        return self.get_response(request)
    
    def process_exception(self, request, exception):
        message = ''
        try:
            message = exception.args[0]
        except:
            pass
        logger.exception(message, exc_info=exception)
        return None
