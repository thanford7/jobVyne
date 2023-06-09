__all__ = ('JobSubscription',)

from django.db import models
from django.db.models import Q, UniqueConstraint

from jvapp.models.abstract import AuditFields, JobVynePermissionsMixin, OwnerFields
from jvapp.models.user import PermissionName


class JobSubscription(AuditFields, OwnerFields, JobVynePermissionsMixin):
    # Subscription can be "owned" by an employer, a specific user, or a job
    employer = models.ForeignKey('Employer', null=True, blank=True, on_delete=models.CASCADE, related_name='job_subscription')
    user = models.ForeignKey('JobVyneUser', null=True, blank=True, on_delete=models.CASCADE, related_name='job_subscription')
    job = models.ForeignKey('EmployerJob', null=True, blank=True, unique=True, on_delete=models.CASCADE, related_name='job_subscription')
    is_single_employer = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    filter_job_title_regex = models.CharField(max_length=500, null=True, blank=True)
    filter_exclude_job_title_regex = models.CharField(max_length=500, null=True, blank=True)
    filter_location = models.ManyToManyField('Location')
    filter_range_miles = models.SmallIntegerField(null=True, blank=True)
    filter_job = models.ManyToManyField('EmployerJob')
    filter_employer = models.ManyToManyField('Employer')
    filter_remote_type_bit = models.SmallIntegerField(null=True, blank=True)  # See REMOTE_TYPES
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['employer'], condition=Q(is_single_employer=True), name='unique_employer')
        ]
    
    def _jv_can_create(self, user):
        return (
            user.is_admin
            # TODO: Add new employer permission to manage job subscriptions
            or (
                self.employer_id
                and user.employer_id == self.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_SETTINGS.value, user.employer_id)
            )
            or (
                self.user_id
                and user.id == self.user_id
            )
        )
    
    @property
    def is_employer_subscription(self):
        return self.is_single_employer and self.employer_id
