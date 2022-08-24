from enum import Enum

from django.db import models
from django.db.models import Q

from jvapp.models.abstract import AuditFields, JobVynePermissionsMixin

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


class SocialContentItem(models.Model, JobVynePermissionsMixin):
    employer = models.ForeignKey('Employer', null=True, blank=True, on_delete=models.CASCADE, related_name='social_content_item')
    user = models.ForeignKey('JobVyneUser', null=True, blank=True, on_delete=models.CASCADE, related_name='social_content_item')
    content = models.TextField()

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
        
        filter = Q(employer_id=user.employer_id) | Q(user_id=user.id)
        return query.filter(filter)
    
    def _jv_can_create(self, user):
        from jvapp.models import PermissionName  # Avoid circular import
        return (
                user.is_admin
                or (
                    self.employer_id == user.employer_id
                    and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_CONTENT.value, user.employer_id)
                )
                or (
                    self.user_id == user.id
                    and ((not user.employer_id) or user.has_employer_permission(PermissionName.ADD_EMPLOYEE_CONTENT.value, user.employer_id))
                )
        )
