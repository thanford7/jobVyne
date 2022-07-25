from django.core.validators import FileExtensionValidator
from django.db import models

from jvapp.models._customDjangoField import LowercaseCharField
from jvapp.models.abstract import ALLOWED_UPLOADS_ALL, AuditFields, JobVynePermissionsMixin
from jvapp.models.location import Country, State
from jvapp.models.user import PermissionName


__all__ = (
    'Employer', 'EmployerJob', 'EmployerSize', 'JobDepartment',
    'EmployerAuthGroup', 'EmployerPermission', 'EmployerFile', 'EmployerFileTag'
)


def getEmployerUploadLocation(instance, filename):
    return f'employers/{instance.employer_id}/{filename}'


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


#If multiple records have is_default = True, tie break will go to:
# (1) employer is not null
# (2) the greatest id
def is_default_auth_group(auth_group, auth_groups):
    if not auth_group.is_default:
        return False
    
    potential_defaults = [g for g in auth_groups if g.is_default and g.user_type_bit == auth_group.user_type_bit]
    potential_defaults.sort(key=lambda group: (-bool(group.employer_id), -group.id))
    return potential_defaults[0].id == auth_group.id
    
    
class EmployerAuthGroup(models.Model, JobVynePermissionsMixin):
    name = models.CharField(max_length=150)
    # If true, this auth group will be automatically added to users with the associated user_type_bit
    # Only one auth group will be automatically added per user_type_bit
    is_default = models.BooleanField(default=False)
    user_type_bit = models.SmallIntegerField()
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, null=True, blank=True)
    permissions = models.ManyToManyField('EmployerPermission')
    
    class Meta:
        unique_together = ('name', 'employer')
        
    def __str__(self):
        return f'{self.employer.employerName if self.employer else "<General>"}-{self.name}'
        
    def jv_check_can_update_permissions(self, user):
        if not self.jv_can_update_permissions(user):
            self._raise_permission_error(PermissionName.CHANGE_PERMISSIONS.value)
            
    def jv_can_update_permissions(self, user):
        return user.has_employer_permission(PermissionName.CHANGE_PERMISSIONS.value)
        
    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                self.employer_id == user.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_PERMISSION_GROUPS.value)
            )
        )
    
    def _jv_can_edit(self, user):
        if not self._jv_can_create(user):
            return False
        
        return bool(self.employer_id) or user.is_admin
    
    def _jv_can_delete(self, user):
        return self._jv_can_edit(user)
    
    
class EmployerPermission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    user_type_bits = models.SmallIntegerField()
    
    def __str__(self):
        return self.name
    
    
class EmployerFile(AuditFields):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, related_name='file')
    file = models.FileField(
        upload_to=getEmployerUploadLocation,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOADS_ALL)]
    )
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField('EmployerFileTag')
    
    
class EmployerFileTag(models.Model):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, related_name='file_tag')
    name = LowercaseCharField(max_length=100)
    
    class Meta:
        unique_together = ('employer', 'name')


class EmployerSize(models.Model):
    size = models.CharField(max_length=25, unique=True)
    
    def __str__(self):
        return self.size
    
    
class JobDepartment(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
