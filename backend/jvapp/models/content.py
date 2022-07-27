from enum import Enum

from django.db import models

from jvapp.models.abstract import AuditFields

__all__ = ('ContentType', 'ContentItem')


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
    item_parts = models.JSONField()
    
    class Meta:
        ordering = ('orderIdx', )
