from enum import Enum

from django.db import models

from jvapp.models.abstract import AuditFields

__all__ = ('ContentType', 'ContentItem', 'SocialContentItem')


class ContentType(Enum):
    TEXT = 'TEXT'
    ICON = 'ICON',
    CAROUSEL = 'CAROUSEL'
    ACCORDION = 'ACCORDION'
    MESSAGE = 'MESSAGE'


class ContentItem(AuditFields):
    header = models.CharField(max_length=250, null=True, blank=True)
    orderIdx = models.SmallIntegerField(null=True, blank=True)
    type = models.CharField(max_length=15)
    config = models.JSONField(null=True, blank=True)
    item_parts = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ('orderIdx', )


class SocialContentItem(models.Model):
    employer = models.ForeignKey('Employer', null=True, blank=True, on_delete=models.CASCADE, related_name='social_content_item')
    user = models.ForeignKey('JobVyneUser', null=True, blank=True, on_delete=models.CASCADE, related_name='social_content_item')
    content = models.TextField()
