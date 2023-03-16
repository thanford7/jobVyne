from enum import Enum

from django.core.validators import FileExtensionValidator
from django.db import models

from jvapp.models._customDjangoField import LowercaseCharField
from jvapp.models.abstract import ALLOWED_UPLOADS_ALL, AuditFields, JobVynePermissionsMixin, OwnerFields
from jvapp.models.user import PermissionName

__all__ = (
    'Employer', 'EmployerAts', 'EmployerJob', 'EmployerSize', 'JobDepartment',
    'EmployerAuthGroup', 'EmployerPermission', 'EmployerFile', 'EmployerFileTag',
    'EmployerPage', 'EmployerReferralBonusRule', 'EmployerReferralBonusRuleModifier',
    'EmployerSubscription', 'EmployerReferralRequest'
)


def get_employer_upload_location(instance, filename):
    employer_id = instance.employer_id if hasattr(instance, 'employer_id') else instance.id
    return f'employers/{employer_id}/{filename}'


class Employer(AuditFields, OwnerFields, JobVynePermissionsMixin):
    ORG_TYPE_EMPLOYER = 0x1
    ORG_TYPE_GROUP = 0x2
    ORG_TYPE_AGENCY = 0x4
    
    organization_type = models.SmallIntegerField(default=ORG_TYPE_EMPLOYER)
    employer_name = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to=get_employer_upload_location, null=True, blank=True)
    employer_size = models.ForeignKey('EmployerSize', null=True, blank=True, on_delete=models.SET_NULL)
    email_domains = models.CharField(max_length=200, null=True, blank=True)  # CSV list of allowed email domains
    notification_email = models.CharField(max_length=50, null=True, blank=True)  # If present, an email will be sent to this address when a new application is created
    company_jobs_page_url = models.CharField(max_length=100, null=True, blank=True)  # Used to redirect users if employer's account is inactive
    is_manual_job_entry = models.BooleanField(default=False, blank=True)  # Whether HR users can manually add jobs
    is_use_job_url = models.BooleanField(default=False, blank=True)  # For employers with no relationship to JobVyne we need to redirect users to the job page
    
    # Brand colors - saved in hex form (e.g. #32a852)
    color_primary = models.CharField(max_length=9, null=True, blank=True)
    color_secondary = models.CharField(max_length=9, null=True, blank=True)
    color_accent = models.CharField(max_length=9, null=True, blank=True)
    
    # Bonus rules
    default_bonus_amount = models.FloatField(null=True, blank=True)
    default_bonus_currency = models.ForeignKey('Currency', on_delete=models.PROTECT, to_field='name', default='USD')
    
    # Billing
    stripe_customer_key = models.CharField(max_length=25, null=True, blank=True, unique=True)
    street_address = models.CharField(max_length=150, null=True, blank=True)
    street_address_2 = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    billing_email = models.EmailField(null=True, blank=True)
    
    # Job scraping
    has_job_scraper = models.BooleanField(default=False, blank=True)
    last_job_scrape_success_dt = models.DateTimeField(null=True, blank=True)
    has_job_scrape_failure = models.BooleanField(default=False, blank=True)
    
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
    
    
class EmployerSubscription(models.Model, JobVynePermissionsMixin):
    
    class SubscriptionStatus(Enum):
        ACTIVE = 'active'
        TRIALING = 'trialing'
        INCOMPLETE = 'incomplete'
        EXPIRED = 'incomplete_expired'
        CANCELED = 'canceled'
        PAST_DUE = 'past_due'
        UNPAID = 'unpaid'
        
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, related_name='subscription')
    # Stripe Key will be null if a JobVyne admin manually added a subscription for the employer
    stripe_key = models.CharField(max_length=30, null=True, blank=True, unique=True)
    status = models.CharField(max_length=20)
    employee_seats = models.PositiveIntegerField()
    
    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                user.employer_id == self.id
                and user.has_employer_permission(PermissionName.MANAGE_BILLING_SETTINGS.value, user.employer_id)
            )
        )
    
    
class EmployerAts(AuditFields, JobVynePermissionsMixin):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, related_name='ats_cfg')
    name = models.CharField(max_length=20)

    # Credentials used by Greenhouse, Lever
    email = models.EmailField(null=True, blank=True)
    api_key = models.CharField(max_length=50, null=True, blank=True)
    
    # Credentials used by Lever
    access_token = models.CharField(max_length=1600, null=True, blank=True)
    refresh_token = models.CharField(max_length=1600, null=True, blank=True)
    access_token_expire_dt = models.DateTimeField(null=True, blank=True)
    refresh_token_expire_dt = models.DateTimeField(null=True, blank=True)
    
    # Custom fields used by Greenhouse
    job_stage_name = models.CharField(max_length=50, null=True, blank=True)
    employment_type_field_key = models.CharField(max_length=30, null=True, blank=True)
    salary_range_field_key = models.CharField(max_length=30, null=True, blank=True)
    
    # Webhooks
    is_webhook_enabled = models.BooleanField(default=False)
    webhook_stage_change_key = models.CharField(max_length=50, null=True, blank=True)
    webhook_stage_change_token = models.CharField(max_length=50, null=True, blank=True)
    webhook_archive_key = models.CharField(max_length=50, null=True, blank=True)
    webhook_archive_token = models.CharField(max_length=50, null=True, blank=True)
    webhook_hire_key = models.CharField(max_length=50, null=True, blank=True)
    webhook_hire_token = models.CharField(max_length=50, null=True, blank=True)
    webhook_delete_key = models.CharField(max_length=50, null=True, blank=True)
    webhook_delete_token = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        unique_together = ('employer', 'name')
    
    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                user.employer_id == self.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_SETTINGS.value, user.employer_id)
            )
        )


class EmployerJob(AuditFields, OwnerFields, JobVynePermissionsMixin):
    UPDATE_FIELDS = [
        'job_title', 'job_description', 'job_department', 'open_date', 'close_date',
        'salary_currency', 'salary_interval', 'salary_floor', 'salary_ceiling', 'employment_type',
        'ats_job_key', 'modified_dt'
    ]
    
    class SalaryInterval(Enum):
        YEAR = 'year'
        MONTH = 'month'
        WEEK = 'week'
        DAY = 'day'
        HOUR = 'hour'
        ONCE = 'once'
    
    employer = models.ForeignKey(Employer, on_delete=models.PROTECT, related_name='employer_job')
    job_title = models.CharField(max_length=200)
    job_description = models.TextField(null=True, blank=True)
    job_department = models.ForeignKey('JobDepartment', on_delete=models.SET_NULL, null=True, blank=True)
    open_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    salary_currency = models.ForeignKey('Currency', on_delete=models.PROTECT, null=True, blank=True, to_field='name', default='USD', related_name='job')
    salary_interval = models.CharField(max_length=20, null=True, blank=True)
    salary_floor = models.FloatField(null=True, blank=True)
    salary_ceiling = models.FloatField(null=True, blank=True)
    referral_bonus = models.FloatField(null=True, blank=True)
    referral_bonus_currency = models.ForeignKey('Currency', on_delete=models.PROTECT, to_field='name', default='USD')
    employment_type = models.CharField(max_length=30, null=True, blank=True)
    locations = models.ManyToManyField('Location')
    application_url = models.CharField(max_length=300, null=True, blank=True)  # Used as a fallback when we don't have an ATS integration with an employer
    is_scraped = models.BooleanField(default=False, blank=True)
    
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

    def get_key(self):
        return self.generate_job_key(self.job_title, tuple(l.id for l in self.locations.all()))
    
    @staticmethod
    def generate_job_key(job_title, location_ids: tuple):
        """Used to compare jobs that have not yet been saved to ones that have been saved.
        This way, we don't have to save job locations before determining whether jobs are equivalent
        """
        return job_title, location_ids
    
    @property
    def is_remote(self):
        for location in self.locations.all():
            if location.is_remote:
                return True
            
        return False
    
    
class EmployerReferralRequest(AuditFields, JobVynePermissionsMixin):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='referral_request')
    email_subject = models.CharField(max_length=255)
    email_body = models.TextField()
    departments = models.ManyToManyField('JobDepartment')
    cities = models.ManyToManyField('City')
    states = models.ManyToManyField('State')
    countries = models.ManyToManyField('Country')
    jobs = models.ManyToManyField('EmployerJob')

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
    
        return query.filter(employer_id=user.employer_id)
    
    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                self.employer_id == user.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_CONTENT.value, user.employer_id)
            )
        )


class EmployerReferralBonusRule(AuditFields, OwnerFields, JobVynePermissionsMixin):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='referral_bonus_rule')
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
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
