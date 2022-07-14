from django.db import models

from jvapp.models.abstract import AuditFields, JobVynePermissionsMixin
from jvapp.models.location import Country, State


__all__ = ('Employer', 'EmployerJob', 'EmployerSize', 'JobDepartment', 'EmployerAuthGroup', 'EmployerPermission')


class Employer(AuditFields):
    employerName = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='logos', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    employerSize = models.ForeignKey('EmployerSize', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.employerName
    
    
class EmployerJob(AuditFields):
    employer = models.ForeignKey(Employer, on_delete=models.PROTECT, related_name='employerJob')
    jobTitle = models.CharField(max_length=100)
    jobDescription = models.TextField()
    jobDepartment = models.ForeignKey('JobDepartment', on_delete=models.SET_NULL, null=True, blank=True)
    openDate = models.DateField(null=True, blank=True)
    closeDate = models.DateField(null=True, blank=True)
    salaryFloor = models.FloatField(null=True, blank=True)
    salaryCeiling = models.FloatField(null=True, blank=True)
    referralBonus = models.FloatField(null=True, blank=True)
    isFullTime = models.BooleanField(default=True, blank=True)

    # Location
    isRemote = models.BooleanField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)  # Raw text
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.employer.employerName}-{self.jobTitle}-{self.location}'
    
    class Meta:
        unique_together = ('employer', 'jobTitle', 'location')
        
        
class EmployerAuthGroup(models.Model, JobVynePermissionsMixin):
    name = models.CharField(max_length=150)
    is_default = models.BooleanField(default=False)
    user_type_bit = models.SmallIntegerField()
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, null=True, blank=True)
    permissions = models.ManyToManyField('EmployerPermission')
    
    class Meta:
        unique_together = ('name', 'employer')
        
    def _jv_can_create(self, user):
        from jvapp.models import PermissionName  # Avoid circular import
        
        return (
            user.is_admin
            or (
                self.employer_id == user.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_PERMISSION_GROUPS.value)
            )
        )
    
    
class EmployerPermission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    user_type_bits = models.SmallIntegerField()
    
    def __str__(self):
        return self.name


class EmployerSize(models.Model):
    size = models.CharField(max_length=25, unique=True)
    
    def __str__(self):
        return self.size
    
    
class JobDepartment(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
