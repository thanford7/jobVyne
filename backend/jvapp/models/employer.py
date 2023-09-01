import re
import uuid
from enum import Enum, IntEnum

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils import timezone

from jvapp.models._customDjangoField import LowercaseCharField
from jvapp.models.abstract import ALLOWED_UPLOADS_ALL, AuditFields, JobVynePermissionsMixin, OwnerFields

__all__ = (
    'Employer', 'EmployerAts', 'EmployerJob', 'JobDepartment',
    'EmployerAuthGroup', 'EmployerPermission', 'EmployerFile', 'EmployerFileTag',
    'EmployerReferralBonusRule', 'EmployerReferralBonusRuleModifier',
    'EmployerSubscription', 'EmployerReferralRequest', 'EmployerJobApplicationRequirement',
    'EmployerSlack', 'Taxonomy', 'JobTaxonomy',
)

from jvapp.models.user import JobVyneUser, PermissionName


def get_employer_upload_location(instance, filename):
    employer_id = instance.employer_id if hasattr(instance, 'employer_id') else instance.id
    return f'employers/{employer_id}/{filename}'


class Employer(AuditFields, OwnerFields, JobVynePermissionsMixin):
    ORG_TYPE_EMPLOYER = 0x1
    ORG_TYPE_GROUP = 0x2
    ORG_TYPE_AGENCY = 0x4
    
    organization_type = models.SmallIntegerField(default=ORG_TYPE_EMPLOYER)
    employer_name = models.CharField(max_length=150, unique=True)
    employer_key = models.CharField(max_length=160, unique=True, null=True, blank=True)
    logo = models.ImageField(upload_to=get_employer_upload_location, null=True, blank=True)
    logo_square_88 = models.ImageField(upload_to=get_employer_upload_location, null=True, blank=True)
    email_domains = models.CharField(max_length=200, null=True, blank=True)  # CSV list of allowed email domains
    notification_email = models.CharField(max_length=50, null=True, blank=True)  # If present, an email will be sent to this address when a new application is created
    company_jobs_page_url = models.CharField(max_length=100, null=True, blank=True)  # Used to redirect users if employer's account is inactive
    is_manual_job_entry = models.BooleanField(default=False, blank=True)  # Whether HR users can manually add jobs
    is_use_job_url = models.BooleanField(default=False, blank=True)  # For employers with no relationship to JobVyne we need to redirect users to the job page
    applicant_tracking_system = models.ForeignKey('ApplicantTrackingSystem', null=True, blank=True, on_delete=models.SET_NULL)

    # Company data
    description = models.TextField(null=True, blank=True)
    description_long = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    size_min = models.IntegerField(null=True, blank=True)
    size_max = models.IntegerField(null=True, blank=True)
    ownership_type = models.CharField(max_length=50, null=True, blank=True)
    year_founded = models.IntegerField(null=True, blank=True)
    linkedin_handle = models.CharField(max_length=50, null=True, blank=True)

    # Brand colors - saved in hex form (e.g. #32a852)
    color_primary = models.CharField(max_length=9, null=True, blank=True)
    color_secondary = models.CharField(max_length=9, null=True, blank=True)
    color_accent = models.CharField(max_length=9, null=True, blank=True)
    
    # Bonus rules
    days_after_hire_payout = models.SmallIntegerField(null=True, blank=True)
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

    # User entered Employer through a social platform
    is_user_created = models.BooleanField(default=False)
    
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
    
    @property
    def main_job_board_link(self):
        if self.organization_type == self.ORG_TYPE_EMPLOYER:
            org_type_name = 'co'
        elif self.organization_type == self.ORG_TYPE_GROUP:
            org_type_name = 'group'
        else:
            raise ValueError('This org type is not yet supported')
        return f'{settings.BASE_URL}/{org_type_name}/{self.employer_key}'
    
    @property
    def website_domain(self):
        return self.email_domains.split(',')[0] if self.email_domains else None

    
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
    
    
class EmployerSlack(models.Model, JobVynePermissionsMixin):
    employer = models.ForeignKey('Employer', unique=True, on_delete=models.CASCADE, related_name='slack_cfg')
    oauth_key = models.CharField(max_length=75, unique=True)
    team_key = models.CharField(max_length=20, unique=True, null=True, blank=True)
    team_name = models.CharField(max_length=100, null=True, blank=True)
    enterprise_key = models.CharField(max_length=20, unique=True, null=True, blank=True)
    enterprise_name = models.CharField(max_length=100, null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    jobs_post_channel = models.CharField(max_length=75, null=True, blank=True)
    jobs_post_dow_bits = models.SmallIntegerField(null=True, blank=True)
    jobs_post_tod_minutes = models.SmallIntegerField(null=True, blank=True)
    jobs_post_max_jobs = models.SmallIntegerField(null=True, blank=True)
    referrals_post_channel = models.CharField(max_length=75, null=True, blank=True)
    modal_cfg_is_salary_required = models.BooleanField(default=False)

    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                user.employer_id == self.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_SETTINGS.value, user.employer_id)
            )
        )
    
    
class ApplicantTrackingSystem(models.Model):
    name = models.CharField(max_length=20, unique=True)
    logo = models.ImageField(blank=True, null=True, upload_to='logos')
    
    
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
        
    class EmploymentType(Enum):
        FULL_TIME = 'Full Time'
        PART_TIME = 'Part Time'
        CONTRACT = 'Contract'
        INTERNSHIP = 'Internship'
    
    job_key = models.UUIDField(unique=True, default=uuid.uuid4, db_index=True)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='employer_job')
    job_title = models.CharField(max_length=200)
    job_description = models.TextField(null=True, blank=True)
    job_description_summary = models.TextField(null=True, blank=True)
    responsibilities = models.JSONField(null=True, blank=True)
    qualifications = models.JSONField(null=True, blank=True)
    technical_qualifications = models.JSONField(null=True, blank=True)
    job_department = models.ForeignKey('JobDepartment', on_delete=models.SET_NULL, null=True, blank=True)
    open_date = models.DateField(null=True, blank=True, db_index=True)
    close_date = models.DateField(null=True, blank=True, db_index=True)
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
    qualifications_prompt = models.ForeignKey('AIRequest', null=True, on_delete=models.SET_NULL)

    ats_job_key = models.CharField(max_length=50, null=True, blank=True)

    # For user entered jobs, we want to review and approve before displaying on the website
    is_job_approved = models.BooleanField(default=True, db_index=True)
    
    class Meta:
        # For ordering to use an index, you cannot mix ascending and descending ordering!
        # https://dba.stackexchange.com/questions/11031/order-by-column-should-have-index-or-not
        ordering = ('-open_date', '-id')
        indexes = [
            models.Index('open_date', 'id', name='open_date_id_idx')
        ]
    
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
            or (
                self.created_user_id and self.created_user_id == user.id
            )
        )

    def get_key(self):
        location_ids = [l.id for l in self.locations.all()]
        location_ids.sort()
        return self.generate_job_key(self.job_title, tuple(location_ids))
    
    @property
    def locations_text(self):
        job_locations_text = ''
        for idx, job_location in enumerate(self.locations.all()):
            job_location_text = job_location.text
            if job_location.is_remote and (not re.search('remote|anywhere|virtual', job_location_text, flags=re.IGNORECASE)):
                job_location_text = f'(Remote) {job_location_text}'
            if idx == 0:
                job_locations_text = job_location_text
            elif idx == 3:
                job_locations_text += ', and more'
                break
            else:
                job_locations_text += f', {job_location_text}'
        if not job_locations_text:
            job_locations_text = 'Unknown'
        
        return job_locations_text
    
    @property
    def salary_text(self):
        if not any((self.salary_floor, self.salary_ceiling)):
            return 'Unknown'
        salary_symbol = self.salary_currency.symbol if self.salary_currency else '$'
        salary_text = f'{salary_symbol}{self.get_formatted_salary(self.salary_floor)}'
        if self.salary_ceiling and (self.salary_floor != self.salary_ceiling):
            salary_text += f' - {salary_symbol}{self.get_formatted_salary(self.salary_ceiling)}'
        if self.salary_interval:
            salary_text += f' per {self.salary_interval}'
        return salary_text
    
    def get_formatted_salary(self, salary: float):
        if int(salary) == salary:
            salary = int(salary)
        return f'{salary:,}'
        
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
    
    @property
    def job_department_standardized(self):
        for tax in self.taxonomy.all():
            if tax.taxonomy.tax_type == Taxonomy.TAX_TYPE_PROFESSION:
                return tax.taxonomy.name
        return 'Unknown'
    
    @property
    def is_user_created(self):
        return bool(self.created_user_id)
    
    @property
    def jv_relative_job_url(self):
        return f'/job/{self.job_key}/'
    
    @property
    def preferred_application_url(self):
        if self.employer.is_use_job_url:
            return self.application_url
        else:
            return f'{settings.BASE_URL}{self.jv_relative_job_url}'
    
    @property
    def has_salary(self):
        return bool(self.salary_floor or self.salary_ceiling)
    
    
# Keep in sync with community.js
class ConnectionTypeBit(IntEnum):
    HIRING_MEMBER = 1
    CURRENT_EMPLOYEE = 2
    FORMER_EMPLOYEE = 4
    KNOW_EMPLOYEE = 8
    NO_CONNECTION = 16
    

class EmployerJobConnection(AuditFields):

    user = models.ForeignKey(JobVyneUser, on_delete=models.CASCADE, related_name='job_connection')
    job = models.ForeignKey(EmployerJob, on_delete=models.CASCADE, related_name='job_connection')
    connection_type = models.SmallIntegerField()
    is_allow_contact = models.BooleanField()  # Whether users can contact the connection
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'job'],
                name='unique_user_job'
            ),
        ]


class Taxonomy(models.Model):
    TAX_TYPE_PROFESSION = 'JOB_TITLE'
    TAX_TYPE_INDUSTRY = 'INDUSTRY'
    TAX_TYPE_JOB_LEVEL = 'JOB_LEVEL'
    ALL_TAX_TYPES = [
        TAX_TYPE_PROFESSION,
        TAX_TYPE_INDUSTRY,
        TAX_TYPE_JOB_LEVEL
    ]
    
    tax_type = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=50, unique=True, null=True, blank=True)
    sub_taxonomies = models.ManyToManyField('self', related_name='parent_taxonomy', symmetrical=False)
    # TODO: Add descriptions for job levels category
    description = models.CharField(max_length=2000, null=True, blank=True)
    sort_order = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('tax_type', 'name')

    def __str__(self):
        return f'{self.tax_type}: {self.name}'
    
    def get_unique_key(self):
        return self.tax_type, self.name
    
    @property
    def jobs_url(self):
        if self.tax_type == self.TAX_TYPE_PROFESSION:
            return f'{settings.BASE_URL}/profession/{self.key}'
        return None


class JobTaxonomy(AuditFields):
    job = models.ForeignKey(EmployerJob, on_delete=models.CASCADE, related_name='taxonomy')
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, related_name='job')

    class Meta:
        constraints = [
            # This is what we really want:
            # models.constraints.UniqueConstraint(fields=('job', 'taxonomy__tax_type'), name='job_unique_taxonomy')
            # But this is the best we can do; we'll have to disallow multiple assignments on a single taxonomy type some other way
            models.constraints.UniqueConstraint(fields=('job', 'taxonomy'), name='job_unique_taxonomy'),
        ]

# TODO: Implement model and use in prediction
# class AiPrompt():
#     '''An AI prompt'''
#     pass


class EmployerJobApplicationRequirement(AuditFields, JobVynePermissionsMixin):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_application_requirement')
    application_field = models.CharField(max_length=25)  # based on JobApplicationFields model
    is_required = models.BooleanField()
    is_optional = models.BooleanField()
    is_hidden = models.BooleanField()
    is_locked = models.BooleanField()  # If true, user cannot update
    filter_departments = models.ManyToManyField('JobDepartment')
    filter_jobs = models.ManyToManyField('EmployerJob')
    
    class Meta:
        unique_together = ('employer', 'application_field', 'is_required', 'is_optional', 'is_hidden')
    
    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                self.employer_id == user.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_CONTENT.value, user.employer_id)
            )
        )


class EmployerReferralRequest(AuditFields, JobVynePermissionsMixin):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='referral_request')
    email_subject = models.CharField(max_length=255)
    email_body = models.TextField()

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
    
    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
        
        if user.is_employer and user.is_employer_verified:
            employer_filter = Q(employer_id=user.employer_id) | Q(employer_id__isnull=True)
            return query.filter(employer_filter)
        
        return query.filter(Q(employer_id__isnull=True))
        
    
    def jv_check_can_update_permissions(self, user):
        if not self.jv_can_update_permissions(user):
            self._raise_permission_error(PermissionName.CHANGE_PERMISSIONS.value)
    
    def jv_can_update_permissions(self, user):
        return self.employer_id == user.employer_id and user.has_employer_permission(PermissionName.CHANGE_PERMISSIONS.value, user.employer_id)
    
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


class JobDepartment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
