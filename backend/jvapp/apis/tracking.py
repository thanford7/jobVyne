from datetime import timedelta

from django.contrib.gis.geoip2 import GeoIP2
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user_agents import parse

from jvapp.models import PageView

__all__ = ('PageTrackView',)

geo_locator = GeoIP2()


# Check whether the same IP address viewed the page within this number of minutes
# If so, don't save a new view record. The assumption is that this is just a page refresh
UNIQUE_VIEW_LOOKBACK_MINUTES = 30


class PageTrackView(APIView):
    
    def post(self, request):
        meta = request.META
        pageView = PageView()
        pageView.relative_url = request.data['relative_url']
        pageView.social_link_filter_id = request.data.get('filter_id')
        
        pageView.ip_address = meta.get('HTTP_X_FORWARDED_FOR') or meta.get('REMOTE_ADDR')
        pageView.access_dt = timezone.now()
        
        location_data = None
        if pageView.ip_address:
            try:
                location_data = geo_locator.city(pageView.ip_address)
            except Exception:
                pass
        if location_data:
            pageView.city = location_data['city']
            pageView.country = location_data['country_name']
            pageView.region = location_data['region']
            pageView.latitude = location_data['latitude']
            pageView.longitude = location_data['longitude']
    
        if user_agent_str := meta.get('HTTP_USER_AGENT'):
            user_agent = parse(user_agent_str)
            pageView.browser = user_agent.browser.family
            pageView.browser_version = user_agent.browser.version_string
            pageView.operating_system = user_agent.os.family
            pageView.device_type = user_agent.device.family
            pageView.device_brand = user_agent.device.brand
            pageView.device_model = user_agent.device.model
            pageView.is_mobile = user_agent.is_mobile
            pageView.is_tablet = user_agent.is_tablet
            pageView.is_pc = user_agent.is_pc
            pageView.is_bot = user_agent.is_bot
            
        recent_page_views = PageView.objects.filter(
            relative_url=pageView.relative_url,
            ip_address=pageView.ip_address,
            access_dt__gt=timezone.now() - timedelta(minutes=UNIQUE_VIEW_LOOKBACK_MINUTES)
        )
        
        if not len(recent_page_views):
            pageView.save()
            
        return Response(status=status.HTTP_200_OK)
