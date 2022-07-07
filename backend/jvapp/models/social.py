import uuid

from django.db import models

from jvapp.models._customDjangoField import SeparatedValueField
from jvapp.models.abstract import AuditFields, JobVynePermissionsMixin

__all__ = ('SocialPlatform', 'SocialLinkFilter')


class SocialPlatform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='logos', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
        

class SocialLinkFilter(AuditFields, JobVynePermissionsMixin):
    # Make ID random so people can't randomly guess a unique filter link
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE)
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
    platform = models.ForeignKey('SocialPlatform', on_delete=models.SET_NULL, null=True, blank=True)
    departments = models.ManyToManyField('JobDepartment')
    cities = SeparatedValueField('|', max_length=500, null=True, blank=True)
    states = models.ManyToManyField('State')
    countries = models.ManyToManyField('Country')
    jobs = models.ManyToManyField('EmployerJob')
    
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
