from django.db import models
from django.db.models import Q

from jvapp.models import PermissionName, REMOTE_TYPES
from jvapp.models.abstract import AuditFields, JobVynePermissionsMixin, OwnerFields

__all__ = ('EmployerJobSubscription',)


class EmployerJobSubscription(AuditFields, OwnerFields, JobVynePermissionsMixin):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, related_name='job_subscription')
    is_approved = models.BooleanField(default=False)
    filter_department = models.ManyToManyField('JobDepartment')
    filter_city = models.ManyToManyField('City')
    filter_state = models.ManyToManyField('State')
    filter_country = models.ManyToManyField('Country')
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
        if department_ids := [d.id for d in self.filter_department.all()]:
            job_filter &= Q(job_department_id__in=department_ids)
        if city_ids := [c.id for c in self.filter_city.all()]:
            job_filter &= Q(locations__city_id__in=city_ids)
        if state_ids := [s.id for s in self.filter_state.all()]:
            job_filter &= Q(locations__state_id__in=state_ids)
        if country_ids := [c.id for c in self.filter_country.all()]:
            job_filter &= Q(locations__country_id__in=country_ids)
        if job_ids := [j.id for j in self.filter_job.all()]:
            job_filter &= Q(id__in=job_ids)
        if employer_ids := [e.id for e in self.filter_employer.all()]:
            job_filter &= Q(employer_id__in=employer_ids)
        if self.filter_remote_type_bit == REMOTE_TYPES.NO:
            job_filter &= Q(locations__is_remote=False)
        elif self.filter_remote_type_bit == REMOTE_TYPES.YES:
            job_filter &= Q(locations__is_remote=True)
        return job_filter