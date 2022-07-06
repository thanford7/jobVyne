from django.db import models

from jvapp.models._customDjangoField import SeparatedValueField
from jvapp.models.abstract import AuditFields

__all__ = ('SocialPlatform', 'SocialLinkFilter')


class SocialPlatform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='logos', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
        

class SocialLinkFilter(AuditFields):
    owner = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE)
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
    platform = models.ForeignKey('SocialPlatform', on_delete=models.SET_NULL, null=True, blank=True)
    departments = models.ManyToManyField('JobDepartment')
    cities = SeparatedValueField('|', max_length=500, null=True, blank=True)
    states = models.ManyToManyField('State')
    countries = models.ManyToManyField('Country')
    jobs = models.ManyToManyField('EmployerJob')
