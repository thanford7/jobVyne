from enum import Enum

from django.db import models
from django.db.models import Q
from django.utils import timezone

from jvapp.models.abstract import JobVynePermissionsMixin

__all__ = ('PageView', 'Message', 'MessageRecipient', 'MessageAttachment')


class PageView(models.Model, JobVynePermissionsMixin):
    # page
    relative_url = models.CharField(max_length=100)
    social_link_filter = models.ForeignKey(
        'SocialLinkFilter', on_delete=models.CASCADE, null=True, blank=True, related_name='page_view'
    )
    platform = models.ForeignKey('SocialPlatform', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Unique characteristics
    ip_address = models.CharField(max_length=40, null=True, blank=True)
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

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
    
        filter = Q(social_link_filter__owner_id=user.id)
        if user.is_employer:
            filter |= Q(social_link_filter__employer_id=user.employer_id)
    
        return query.filter(filter)
    
    
class Message(models.Model):
    class MessageType(Enum):
        EMAIL = 'EMAIL'
    
    type = models.CharField(max_length=5)
    subject = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    body_html = models.TextField(null=True, blank=True)
    from_address = models.CharField(max_length=255)
    created_dt = models.DateTimeField()


class MessageAttachment(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name='attachment')
    file = models.FileField(upload_to='message_attachments')
    
    
class MessageRecipient(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name='recipient')
    recipient_address = models.CharField(max_length=255)
    provider_message_key = models.CharField(max_length=80, null=True, blank=True)
    processed_dt = models.DateTimeField(null=True, blank=True)
    error_dt = models.DateTimeField(null=True, blank=True)
    delivered_dt = models.DateTimeField(null=True, blank=True)
    opened_dt = models.DateTimeField(null=True, blank=True)
    clicked_dt = models.DateTimeField(null=True, blank=True)
    error_reason = models.CharField(max_length=500, null=True, blank=True)