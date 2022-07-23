from django.db import models
from django.utils import timezone

__all__ = ('PageView',)


class PageView(models.Model):
    # page
    relative_url = models.CharField(max_length=100)
    social_link_filter = models.ForeignKey(
        'SocialLinkFilter', on_delete=models.CASCADE, null=True, blank=True, related_name='page_view'
    )
    
    # Unique characteristics
    ip_address = models.CharField(max_length=20, null=True, blank=True)
    access_dt = models.DateTimeField(default=timezone.now)
    
    # location
    city = models.CharField(max_length=60, null=True, blank=True)
    country = models.CharField(max_length=60, null=True, blank=True)
    region = models.CharField(max_length=60, null=True, blank=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    
    # user agent
    browser = models.CharField(max_length=60, null=True, blank=True)
    browser_version = models.CharField(max_length=20, null=True, blank=True)
    operating_system = models.CharField(max_length=30, null=True, blank=True)
    device_type = models.CharField(max_length=20, null=True, blank=True)
    device_brand = models.CharField(max_length=40, null=True, blank=True)
    device_model = models.CharField(max_length=40, null=True, blank=True)
    is_mobile = models.BooleanField(null=True, blank=True)
    is_tablet = models.BooleanField(null=True, blank=True)
    is_pc = models.BooleanField(null=True, blank=True)
    is_bot = models.BooleanField(null=True, blank=True)
    