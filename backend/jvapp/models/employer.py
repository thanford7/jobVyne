from enum import Enum

from django.core.validators import FileExtensionValidator
from django.db import models

from jvapp.models._customDjangoField import LowercaseCharField
from jvapp.models.abstract import ALLOWED_UPLOADS_ALL, AuditFields, JobVynePermissionsMixin, OwnerFields
from jvapp.models.user import PermissionName

__all__ = (
    'Employer', 'EmployerAts', 'EmployerJob', 'EmployerSize', 'JobDepartment',
    'EmployerAuthGroup', 'EmployerPermission', 'EmployerFile', 'EmployerFileTag',
    'EmployerPage', 'EmployerReferralBonusRule', 'EmployerReferralBonusRuleModifier'
)


def get_employer_upload_location(instance, filename):
    employer_id = instance.employer_id if hasattr(instance, 'employer_id') else instance.id
    return f'employers/{employer_id}/{filename}'


class Employer(AuditFields, OwnerFields, JobVynePermissionsMixin):
    employer_name = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to=get_employer_upload_location, null=True, blank=True)
    employer_size = models.ForeignKey('EmployerSize', null=True, blank=True, on_delete=models.SET_NULL)
    email_domains = models.CharField(max_length=200, null=True, blank=True)  # CSV list of allowed email domains
    
    # Brand colors - saved in hex form (e.g. #32a852)
    color_primary = models.CharField(max_length=9, null=True, blank=True)
    color_secondary = models.CharField(max_length=9, null=True, blank=True)
    color_accent = models.CharField(max_length=9, null=True, blank=True)
    
    # Bonus rules
    default_bonus_amount = models.FloatField(null=True, blank=True)
    default_bonus_currency = models.ForeignKey('Currency', on_delete=models.PROTECT, to_field='name', default='USD')
    
    def __str__(self):
        return self.employer_name
    
    def _jv_can_create(self, user):
        return user.is_admin
    
    def _jv_can_edit(self, user):
        return (
            user.is_admin
            or (
                user.employer_id == self.id
                and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_SETTINGS.value, user.employer_id)
            )
        )
    
    def _jv_can_delete(self, user):
        return user.is_admin
    
    
class EmployerAts(AuditFields, JobVynePermissionsMixin):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, related_name='ats_cfg')
    name = models.CharField(max_length=20)
    email = models.EmailField()
    api_key = models.CharField(max_length=50)
    
    class Meta:
        unique_together = ('employer', 'name')
    
    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                user.employer_id == self.id
                and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_SETTINGS.value, user.employer_id)
            )
        )


class EmployerJob(AuditFields, OwnerFields, JobVynePermissionsMixin):
    UPDATE_FIELDS = [
        'job_title', 'job_description', 'job_department', 'open_date', 'close_date',
        'salary_currency', 'salary_floor', 'salary_ceiling', 'employment_type',
        'ats_job_key', 'modified_dt'
    ]
    
    employer = models.ForeignKey(Employer, on_delete=models.PROTECT, related_name='employer_job')
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    job_department = models.ForeignKey('JobDepartment', on_delete=models.SET_NULL, null=True, blank=True)
    open_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    salary_currency = models.ForeignKey('Currency', on_delete=models.PROTECT, null=True, blank=True, to_field='name', default='USD', related_name='job')
    salary_floor = models.FloatField(null=True, blank=True)
    salary_ceiling = models.FloatField(null=True, blank=True)
    referral_bonus = models.FloatField(null=True, blank=True)
    referral_bonus_currency = models.ForeignKey('Currency', on_delete=models.PROTECT, to_field='name', default='USD')
    employment_type = models.CharField(max_length=30, null=True, blank=True)
    locations = models.ManyToManyField('Location')
    
    ats_job_key = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f'{self.employer.employer_name}-{self.job_title}-{self.id}'
    
    def _jv_can_edit(self, user):
        # For now, the only fields that can be edited from the frontend are the referral bonus fields
        return (
            user.is_admin
            or (
                self.employer_id == user.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_REFERRAL_BONUSES.value, user.employer_id)
            )
        )


class EmployerReferralBonusRule(AuditFields, OwnerFields, JobVynePermissionsMixin):
    employer = models.ForeignKey(Employer, on_delete=models.PROTECT, related_name='referral_bonus_rule')
    order_idx = models.SmallIntegerField()
    include_departments = models.ManyToManyField('JobDepartment', related_name='include_bonus')
    exclude_departments = models.ManyToManyField('JobDepartment', related_name='exclude_bonus')
    include_cities = models.ManyToManyField('City', related_name='include_bonus')
    exclude_cities = models.ManyToManyField('City', related_name='exclude_bonus')
    include_states = models.ManyToManyField('State', related_name='include_bonus')
    exclude_states = models.ManyToManyField('State', related_name='exclude_bonus')
    include_countries = models.ManyToManyField('Country', related_name='include_bonus')
    exclude_countries = models.ManyToManyField('Country', related_name='exclude_bonus')
    include_job_titles_regex = models.CharField(max_length=500, null=True, blank=True)
    exclude_job_titles_regex = models.CharField(max_length=500, null=True, blank=True)
    base_bonus_amount = models.FloatField()
    bonus_currency = models.ForeignKey('Currency', on_delete=models.PROTECT, to_field='name', default='USD')
    days_after_hire_payout = models.SmallIntegerField()
    
    class Meta:
        ordering = ('employer_id', 'order_idx')
    
    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                self.employer_id == user.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_REFERRAL_BONUSES.value, user.employer_id)
            )
        )
    
    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
        
        return query.filter(employer_id=user.employer_id)


class EmployerReferralBonusRuleModifier(models.Model):
    class ModifierType(Enum):
        PERCENT = 'PERCENT'
        NOMINAL = 'NOMINAL'
    
    referral_bonus_rule = models.ForeignKey(EmployerReferralBonusRule, on_delete=models.CASCADE,
                                            related_name='modifier')
    type = models.CharField(max_length=10)
    amount = models.FloatField()
    start_days_after_post = models.SmallIntegerField()
    
    class Meta:
        ordering = ('referral_bonus_rule', 'start_days_after_post')


# If multiple records have is_default = True, tie break will go to:
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
        return f'{self.employer.employer_name if self.employer else "<General>"}-{self.name}'
    
    def jv_check_can_update_permissions(self, user):
        if not self.jv_can_update_permissions(user):
            self._raise_permission_error(PermissionName.CHANGE_PERMISSIONS.value)
    
    def jv_can_update_permissions(self, user):
        return user.has_employer_permission(PermissionName.CHANGE_PERMISSIONS.value, user.employer_id)
    
    def _jv_can_create(self, user):
        return (
                user.is_admin
                or (
                        self.employer_id == user.employer_id
                        and user.has_employer_permission(PermissionName.MANAGE_PERMISSION_GROUPS.value,
                                                         user.employer_id)
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


class EmployerFile(AuditFields, OwnerFields, JobVynePermissionsMixin):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, related_name='file')
    file = models.FileField(
        upload_to=get_employer_upload_location,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOADS_ALL)]
    )
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField('EmployerFileTag')
    
    def __str__(self):
        return self.title
    
    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                self.employer_id == user.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_CONTENT.value, user.employer_id)
            )
        )


class EmployerFileTag(models.Model, JobVynePermissionsMixin):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, related_name='file_tag')
    name = LowercaseCharField(max_length=100)
    
    class Meta:
        unique_together = ('employer', 'name')
    
    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                self.employer_id == user.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_CONTENT.value, user.employer_id)
            )
        )


class EmployerPage(AuditFields, OwnerFields, JobVynePermissionsMixin):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, related_name='profile_page', unique=True)
    is_viewable = models.BooleanField(default=False)
    content_item = models.ManyToManyField('ContentItem')
    
    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                self.employer_id == user.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_CONTENT.value, user.employer_id)
            )
        )


class EmployerSize(models.Model):
    size = models.CharField(max_length=25, unique=True)
    
    def __str__(self):
        return self.size


class JobDepartment(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
