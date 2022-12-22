import uuid

from django.db import models

from jvapp.models.abstract import AuditFields, JobVynePermissionsMixin

__all__ = ('SocialPlatform', 'SocialLinkFilter')


class SocialPlatform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='logos', null=True, blank=True)
    is_displayed = models.BooleanField(default=True)
    sort_order = models.SmallIntegerField(default=1)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('sort_order', )
        

class SocialLinkFilter(AuditFields, JobVynePermissionsMixin):
    # Make ID random so people can't randomly guess a unique filter link
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # The primary social link filter is auto generated when a user is created
    is_primary = models.BooleanField(default=False, blank=True)
    # The default social link filter is used to auto-populate forms
    is_default = models.BooleanField(default=False, blank=True)
    owner = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE)
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
    departments = models.ManyToManyField('JobDepartment')
    cities = models.ManyToManyField('City')
    states = models.ManyToManyField('State')
    countries = models.ManyToManyField('Country')
    jobs = models.ManyToManyField('EmployerJob')
    
    class Meta:
        ordering = ('-is_default', '-modified_dt')
    
    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
        
        if user.is_employee:
            return query.filter(owner_id=user.id)
        
        if user.is_employer:
            return query.filter(employer_id=user.employer_id)
        
        return []
    
    def _jv_can_create(self, user):
        return any((
            user.is_admin,
            user.id == self.owner_id,
            (user.is_employer and self.employer_id == user.employer_id)
        ))

    def get_unique_key(self):
        # Make sure to prefetch related fields!
        departmentIds = tuple(self.departments.all().values_list('id', flat=True).order_by('id'))
        cityIds = tuple(self.cities.all().values_list('id', flat=True).order_by('id'))
        stateIds = tuple(self.states.all().values_list('id', flat=True).order_by('id'))
        countryIds = tuple(self.countries.all().values_list('id', flat=True).order_by('id'))
        jobIds = tuple(self.jobs.all().values_list('id', flat=True).order_by('id'))
        return self.owner_id, departmentIds, cityIds, stateIds, countryIds, jobIds
    