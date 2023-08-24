__all__ = ('PageTrackView',)
import logging
from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.contrib.gis.geoip2 import GeoIP2
from django.db import DataError
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from user_agents import parse

from jvapp.models.employer import Employer
from jvapp.models.social import SocialPlatform
from jvapp.models.tracking import PageView

geo_locator = GeoIP2()
logger = logging.getLogger(__name__)


# Check whether the same IP address viewed the page within this number of minutes
# If so, don't save a new view record. The assumption is that this is just a page refresh
UNIQUE_VIEW_LOOKBACK_MINUTES = 30


def parse_ip_address(address):
    if not address:
        return None
    return address.split(',')[0].strip()


class PageTrackView(APIView):
    permission_classes = [AllowAny]
    
    @method_decorator(csrf_exempt)
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        location_data = None
        try:
            meta = request.META
            page_view = PageView()
            
            if not isinstance(request.user, AnonymousUser):
                page_view.viewer_id = request.user.id
            page_view.relative_url = request.data['relative_url']
            page_view.social_link_id = request.data.get('filter_id')
            params = request.data.get('query') or {}
            page_view.page_owner_id = params.get('connect')
            if employer_key := request.data.get('employer_key'):
                try:
                    page_view.employer = Employer.objects.get(employer_key=employer_key)
                except Employer.DoesNotExist:
                    pass
            if platform_name := params.get('platform'):
                try:
                    page_view.platform = SocialPlatform.objects.get(name__iexact=platform_name)
                except SocialPlatform.DoesNotExist:
                    pass
            
            page_view.ip_address = parse_ip_address(meta.get('HTTP_X_FORWARDED_FOR')) or parse_ip_address(meta.get('REMOTE_ADDR'))
            if page_view.ip_address and len(page_view.ip_address) > 40:
                logger.warning(f'IP Address is too long: {page_view.ip_address}')
                page_view.ip_address = None
            page_view.access_dt = timezone.now()
            
            if page_view.ip_address:
                try:
                    location_data = geo_locator.city(page_view.ip_address)
                except Exception:
                    pass
            if location_data:
                page_view.city = location_data['city']
                page_view.country = location_data['country_name']
                page_view.region = location_data['region']
                page_view.latitude = location_data['latitude']
                page_view.longitude = location_data['longitude']
        
            if user_agent_str := meta.get('HTTP_USER_AGENT'):
                set_user_agent_data(page_view, user_agent_str)
                
            recent_page_views = PageView.objects.filter(
                relative_url=page_view.relative_url,
                ip_address=page_view.ip_address,
                access_dt__gt=timezone.now() - timedelta(minutes=UNIQUE_VIEW_LOOKBACK_MINUTES)
            )
            
            if not len(recent_page_views):
                page_view.save()
        except DataError as e:
            logger.error(e)

        return Response(status=status.HTTP_200_OK, data={
            # 'location': location_data
            'location': {'country_name': 'US'}
        })


def set_user_agent_data(page_view, user_agent_str):
    user_agent = parse(user_agent_str)
    page_view.browser = user_agent.browser.family
    page_view.browser_version = user_agent.browser.version_string
    page_view.operating_system = user_agent.os.family
    page_view.device_type = user_agent.device.family
    page_view.device_brand = user_agent.device.brand
    page_view.device_model = user_agent.device.model
    page_view.is_mobile = user_agent.is_mobile
    page_view.is_tablet = user_agent.is_tablet
    page_view.is_pc = user_agent.is_pc
    page_view.is_bot = user_agent.is_bot
