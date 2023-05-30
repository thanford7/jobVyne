from django.db import models
from django.db.models import Q

from jvapp.apis.social import SocialLinkJobsView
from jvapp.models import PermissionName, REMOTE_TYPES
from jvapp.models.abstract import AuditFields, JobVynePermissionsMixin, OwnerFields

__all__ = ('EmployerJobSubscription',)

from jvapp.serializers.location import get_serialized_location


class EmployerJobSubscription(AuditFields, OwnerFields, JobVynePermissionsMixin):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, related_name='job_subscription')
    is_approved = models.BooleanField(default=False)
    filter_job_title_regex = models.CharField(max_length=500, null=True, blank=True)
    filter_exclude_job_title_regex = models.CharField(max_length=500, null=True, blank=True)
    filter_location = models.ManyToManyField('Location')
    filter_range_miles = models.SmallIntegerField(null=True, blank=True)
    filter_job = models.ManyToManyField('EmployerJob')
    filter_employer = models.ManyToManyField('Employer')
    filter_remote_type_bit = models.SmallIntegerField(null=True, blank=True)  # See REMOTE_TYPES
    
    def _jv_can_create(self, user):
        return (
                user.is_admin
                # TODO: Add new employer permission to manage job subscriptions
                or (
                        user.employer_id == self.employer_id
                        and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_SETTINGS.value, user.employer_id)
                )
        )
    
    def get_job_filter(self):
        job_filter = Q()
        if self.filter_job_title_regex:
            job_filter &= Q(job_title__iregex=f'^.*({self.filter_job_title_regex}).*$')
        if self.filter_exclude_job_title_regex:
            job_filter &= ~Q(job_title__iregex=f'^.*({self.filter_exclude_job_title_regex}).*$')
        if job_ids := [j.id for j in self.filter_job.all()]:
            job_filter &= Q(id__in=job_ids)
        if employer_ids := [e.id for e in self.filter_employer.all()]:
            job_filter &= Q(employer_id__in=employer_ids)
            
        location_dicts = [get_serialized_location(l) for l in self.filter_location.all()]
        combined_location_filter = None
        if location_dicts:
            for location_dict in location_dicts:
                location_filter = SocialLinkJobsView.get_location_filter(
                    location_dict, self.filter_remote_type_bit or 0, self.filter_range_miles
                )
                if not combined_location_filter:
                    combined_location_filter = location_filter
                else:
                    combined_location_filter |= location_filter
        else:
            combined_location_filter = SocialLinkJobsView.get_location_filter(
                None, self.filter_remote_type_bit or 0, None
            )
        job_filter &= combined_location_filter
        return job_filter
