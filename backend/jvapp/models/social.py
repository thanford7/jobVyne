import uuid

from django.db import models
from django.db.models import Q

from jvapp.models._customDjangoField import LowercaseCharField
from jvapp.models.abstract import AuditFields, JobVynePermissionsMixin

__all__ = ('SocialPlatform', 'SocialLinkFilter', 'SocialLinkTag')


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
    is_archived = models.BooleanField(default=False, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    # If no owner, this is an employer owned link
    owner = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, null=True, blank=True)
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
    departments = models.ManyToManyField('JobDepartment')
    cities = models.ManyToManyField('City')
    states = models.ManyToManyField('State')
    countries = models.ManyToManyField('Country')
    jobs = models.ManyToManyField('EmployerJob')
    tags = models.ManyToManyField('SocialLinkTag')
    
    class Meta:
        ordering = ('-is_default', '-modified_dt')
    
    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
        
        link_filter = Q(owner_id=user.id)
        if user.is_employer:
            link_filter |= (Q(employer_id=user.employer_id) & Q(owner_id__isnull=True))
        
        return query.filter(link_filter)
    
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
        return self.owner_id, self.employer_id, self.name, departmentIds, cityIds, stateIds, countryIds, jobIds
    
    
class SocialLinkTag(models.Model, JobVynePermissionsMixin):
    owner = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, null=True, blank=True)
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, null=True, blank=True)
    tag_name = LowercaseCharField(max_length=20)
    
    class Meta:
        unique_together = (
            ('employer_id', 'tag_name'),
            ('owner_id', 'tag_name')
        )

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
    
        link_filter = Q(owner_id=user.id)
        if user.is_employer:
            link_filter |= Q(employer_id=user.employer_id)
    
        return query.filter(link_filter)

    def _jv_can_create(self, user):
        return any((
            user.is_admin,
            user.id == self.owner_id,
            (user.is_employer and self.employer_id == user.employer_id)
        ))
