__all__ = (
    'CustomUserManager', 'JobVyneUser', 'PermissionName', 'UserUnknownEmployer',
    'UserEmployerPermissionGroup', 'UserFile', 'UserEmployerCandidate',
    'UserEmployeeProfileResponse', 'UserEmployeeProfileQuestion', 'UserNotificationPreference',
    'UserApplicationReview'
)
from collections import defaultdict
from enum import Enum, IntEnum

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, UniqueConstraint
from django.utils import crypto, timezone
from django.utils.translation import gettext_lazy as _

from jvapp.models.abstract import ALLOWED_UPLOADS_ALL, AuditFields, JobVynePermissionsMixin
from jvapp.models.location import REMOTE_TYPES
from jvapp.serializers.location import get_serialized_location
from jvapp.utils.email import get_domain_from_email
from jvapp.utils.file import get_user_upload_location
from jvapp.utils.security import generate_user_token, get_uid_from_user


def generate_password():
    return crypto.get_random_string(length=30, allowed_chars=crypto.RANDOM_STRING_CHARS + '!@#$%^&*()-+=')


# Keep in sync with frontend user-types
# Update migration_permissions.py and add a new migration
class PermissionName(Enum):
    MANAGE_USER = 'Manage users'
    CHANGE_PERMISSIONS = 'Change user permissions'
    MANAGE_PERMISSION_GROUPS = 'Manage custom permission groups'
    MANAGE_EMPLOYER_CONTENT = 'Manage employer content'
    MANAGE_EMPLOYER_JOBS = 'Manage employer jobs'
    MANAGE_REFERRAL_BONUSES = 'Manage employee referral bonuses'
    ADD_EMPLOYEE_CONTENT = 'Add personal employee content'
    MANAGE_BILLING_SETTINGS = 'Manage billing settings'
    MANAGE_EMPLOYER_SETTINGS = 'Manage employer settings'
    

USER_MANAGEMENT_PERMISSIONS = [
    PermissionName.MANAGE_USER.value,
    PermissionName.CHANGE_PERMISSIONS.value,
]


# Update migration_permissions.py and add a new migration
class StandardPermissionGroups(Enum):
    ADMIN = 'Admin'
    HR = 'HR Professional'
    EMPLOYEE = 'Employee'
    INFLUENCER = 'Influencer'
    JOB_SEEKER = 'Job Seeker'


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        from jvapp.models.employer import Employer
        from jvapp.apis.employer import EmployerSubscriptionView, EmployerFromDomainView
        
        if not email:
            raise ValueError(_('Email must be set'))
        email = self.normalize_email(email)
        if not 'employer_id' in extra_fields:
            try:
                matched_employers = EmployerFromDomainView.get_employers_from_email(email)
                if len(matched_employers) == 1:
                    extra_fields['employer_id'] = matched_employers[0]['id']
            except ValueError:
                pass
        
        extra_fields['user_type_bits'] = extra_fields.get('user_type_bits') or 0
        user = self.model(email=email, **extra_fields)
        if password:
            validate_password(password, user=user)
        user.set_password(password or generate_password())
        
        # If user is employee, make sure the employer has enough seats in their subscription
        if user.employer_id:
            employer = Employer.objects.prefetch_related('subscription').get(id=user.employer_id)
            subscription = EmployerSubscriptionView.get_subscription(employer)
            active_employees = EmployerSubscriptionView.get_active_employees(employer)
            if not subscription or subscription.employee_seats <= active_employees:
                user.has_employee_seat = False
                
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields['user_type_bits'] = JobVyneUser.USER_TYPE_ADMIN | JobVyneUser.USER_TYPE_CANDIDATE | JobVyneUser.USER_TYPE_EMPLOYEE | JobVyneUser.USER_TYPE_EMPLOYER

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class JobVyneUser(AbstractUser, JobVynePermissionsMixin):
    # Keep in sync with frontend auth-store
    USER_TYPE_ADMIN = 0x1
    USER_TYPE_CANDIDATE = 0x2  # Allows users to save their info so they can apply to jobs with existing info
    USER_TYPE_EMPLOYEE = 0x4
    USER_TYPE_INFLUENCER = 0x8
    USER_TYPE_EMPLOYER = 0x10
    
    JOB_SEARCH_TYPE_ACTIVE = 0x1
    JOB_SEARCH_TYPE_PASSIVE = 0x2
    
    DEFAUL_JOB_SEARCH_RANGE_MILES = 50
    
    # Keep in sync with community.js member types
    MEMBER_TYPE_JOB_SEEKER = 0x1
    MEMBER_TYPE_HIRING_MGR = 0x2
    
    ALL_USER_TYPES = [
        USER_TYPE_ADMIN,
        USER_TYPE_CANDIDATE,
        USER_TYPE_EMPLOYEE,
        USER_TYPE_INFLUENCER,
        USER_TYPE_EMPLOYER
    ]
    
    # Permissions for these user types must be approved by another user with the appropriate privileges
    USER_TYPES_APPROVAL_REQUIRED = [USER_TYPE_EMPLOYER]
    
    username = None
    date_joined = None
    email = models.EmailField(_('email address'), unique=True)
    user_key = models.CharField(max_length=160, unique=True, null=True, blank=True)
    linkedin_url = models.CharField(max_length=200, null=True, blank=True)
    professional_site_url = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=get_user_upload_location, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    business_email = models.EmailField(_('business email address'), unique=True, null=True, blank=True)
    is_business_email_verified = models.BooleanField(default=False)
    
    # To filter on user_type_bits:
    #   any: user_type_bits__lt=F('user_type_bits') + (1 * F('user_type_bits').bitand(user_type_bits))
    #   all: user_type_bits=1 * F('user_type_bits').bitand(user_type_bits)
    user_type_bits = models.SmallIntegerField(default=0)
    employer = models.ForeignKey('Employer', on_delete=models.SET_NULL, null=True, related_name='employee')
    is_employer_owner = models.BooleanField(default=False, blank=True)
    is_employer_deactivated = models.BooleanField(default=False, blank=True)
    has_employee_seat = models.BooleanField(default=True, blank=True)  # If employer's subscription has run out of seats, this will be false
    created_dt = models.DateTimeField(_("date created"), default=timezone.now)
    modified_dt = models.DateTimeField(_("date modified"), default=timezone.now)
    
    # Employee data
    is_profile_viewable = models.BooleanField(default=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    profession = models.ForeignKey('Taxonomy', null=True, blank=True, on_delete=models.SET_NULL)
    employment_start_date = models.DateField(null=True, blank=True)
    
    is_share_connections = models.BooleanField(default=True)
    home_location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)
    work_remote_type_bit = models.SmallIntegerField(default=REMOTE_TYPES.NO.value | REMOTE_TYPES.YES.value)
    job_search_type_bit = models.SmallIntegerField(default=0)
    is_job_search_visible = models.BooleanField(default=False)
    job_search_levels = models.ManyToManyField('Taxonomy', related_name='level_job_seeker')
    job_search_industries = models.ManyToManyField('Taxonomy', related_name='industry_job_seeker')
    job_search_professions = models.ManyToManyField('Taxonomy', related_name='profession_job_seeker')
    job_search_qualifications = models.CharField(max_length=1000, null=True, blank=True)
    membership_groups = models.ManyToManyField('Employer', related_name='group_member')
    membership_professions = models.ManyToManyField('Taxonomy', related_name='profession_member')
    membership_employers = models.ManyToManyField('Employer', related_name='employer_member')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def has_employer_permission(self, permission_name: str or list, employer_id: int, is_all_true: bool = True):
        """Check if user has the specified permission
        :param permission_name: A property of PermissionName class
        :param employer_id
        :param is_all_true: If true, all permissions must be true.
            Otherwise if one permission is true, the func will return true
        """
        if isinstance(permission_name, str):
            permission_name = [permission_name]
        check_method = all if is_all_true else any
        permissions_by_employer = self.get_permissions_by_employer()
        permission_names = [p.name for p in permissions_by_employer.get(employer_id) or []]
        return check_method((name in permission_names for name in permission_name))
    
    def get_reset_password_link(self):
        uid = get_uid_from_user(self)
        token = generate_user_token(self, 'email')
        return f'{settings.BASE_URL}/password-reset/{uid}/{token}'

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
        
        if user.is_employer and user.is_employer_verified:
            return query.filter(employer_id=user.employer_id)
        
        return query.filter(id=user.id)
    
    def _jv_can_create(self, user):
        return user.is_admin or (
            user.has_employer_permission(PermissionName.MANAGE_USER.value, user.employer_id)
            and self.employer_id == user.employer_id
        )
    
    def _jv_can_edit(self, user):
        return self._jv_can_create(user) or self.id == user.id
    
    def _jv_can_delete(self, user):
        return user.is_admin or self.id == user.id

    def get_user_employer_permissions(self, is_include_non_approved=False):
        filter = Q() if is_include_non_approved else Q(is_employer_approved=True)
        return self.employer_permission_group \
            .select_related('permission_group') \
            .prefetch_related('permission_group__permissions') \
            .filter(filter)

    # Note there is a performance penalty if permission_groups is not provided since it requires a DB fetch
    def get_permissions_by_employer(self, permission_groups=None, is_include_non_approved=False):
        employer_permission_groups = permission_groups or self.get_user_employer_permissions(is_include_non_approved)
        permissions = defaultdict(list)
        for employer_permission_group in employer_permission_groups:
            for permission in employer_permission_group.permission_group.permissions.all():
                permissions[employer_permission_group.employer_id].append(permission)
        return permissions

    # Note there is a performance penalty if permission_groups is not provided since it requires a DB fetch
    def get_employer_permission_groups_by_employer(self, permission_groups=None, is_include_non_approved=False):
        employer_permission_groups = permission_groups or self.get_user_employer_permissions(is_include_non_approved)
        groups = defaultdict(list)
        for employer_permission_group in employer_permission_groups:
            groups[employer_permission_group.employer_id].append(employer_permission_group)
        return groups
    
    @property
    def full_name(self):
        return ' '.join([n for n in [self.first_name, self.last_name] if n])
    
    @property
    def emails(self):
        emails = [self.email]
        if self.business_email:
            emails.append(self.business_email)
        return emails
    
    @property
    def is_admin(self):
        return bool(self.user_type_bits & self.USER_TYPE_ADMIN)
    
    @property
    def is_candidate(self):
        return bool(self.user_type_bits & self.USER_TYPE_CANDIDATE)
    
    @property
    def is_employee(self):
        return bool(self.user_type_bits & self.USER_TYPE_EMPLOYEE)
    
    @property
    def is_influencer(self):
        return bool(self.user_type_bits & self.USER_TYPE_INFLUENCER)
    
    @property
    def is_employer(self):
        return bool(self.user_type_bits & self.USER_TYPE_EMPLOYER)
    
    @property
    def is_active_employee(self):
        return self.has_employee_seat and (not self.is_employer_deactivated)
    
    @property
    def is_hiring_manager(self):
        from jvapp.models.employer import ConnectionTypeBit  # Avoid circular import
        return any((
            ec.connection_type & ConnectionTypeBit.HIRING_MEMBER
            for ec in self.employer_connection.all()
        ))
    
    @property
    def is_can_contact(self):
        return any((ec.is_allow_contact for ec in self.employer_connection.all())) or self.is_job_search_visible

    @property
    def is_employer_verified(self):
        if self.is_employer_owner and self.is_email_verified:
            return True
        if not self.employer_id or not self.employer.email_domains:
            return False
    
        return (
            (self.is_email_verified and self.is_email_employer_permitted)
            or (
                    self.business_email
                    and self.is_business_email_verified
                    and get_domain_from_email(self.business_email) in self.employer.email_domains
            )
        )
    
    @property
    def is_email_employer_permitted(self):
        if self.is_employer_owner or self.is_admin:
            return True
        
        if not self.employer_id or not self.employer.email_domains:
            return False
        
        return get_domain_from_email(self.email) in (self.employer.email_domains + 'jobvyne.com')

    @property
    def is_business_email_employer_permitted(self):
        if not self.employer_id or not self.employer.email_domains:
            return False
    
        return self.business_email and get_domain_from_email(self.business_email) in self.employer.email_domains
    
    @property
    def preferred_jobs_filter(self):
        from jvapp.apis.job_subscription import JobSubscriptionView
        from jvapp.apis.social import SocialLinkJobsView
        
        preferred_employers = Q(employer__in=self.membership_employers.all())
        preferred_professions = Q(taxonomy__taxonomy__in=JobSubscriptionView.get_parent_and_child_professions(self.job_search_professions.all()))
        jobs_filter = preferred_employers & preferred_professions
        if self.home_location_id:
            location_dict = get_serialized_location(self.home_location)
            location_filter = SocialLinkJobsView.get_location_filter(
                location_dict, self.work_remote_type_bit, self.DEFAUL_JOB_SEARCH_RANGE_MILES
            )
            jobs_filter &= location_filter
        # Consider adding job search level and job search industries
        return jobs_filter
    
    @property
    def contact_email(self):
        return self.business_email or self.email
    
    
class UserSlackProfile(models.Model):
    user = models.ForeignKey('JobVyneUser', null=False, blank=False, related_name='slack_profile', on_delete=models.CASCADE)
    user_key = models.CharField(max_length=20)
    team_key = models.CharField(max_length=20)
    # The datetime when JobVyne posted that this user was looking for a job
    job_seeker_post_dt = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user_key', 'team_key'],
                name='unique_user'
            ),
        ]


class UserFile(models.Model, JobVynePermissionsMixin):
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='file')
    file = models.FileField(
        upload_to=get_user_upload_location,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOADS_ALL)]
    )
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    
    def _jv_can_create(self, user):
        return self.user_id == user.id

    
class UserSocialCredential(models.Model):
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='social_credential')
    access_token = models.CharField(max_length=1000)
    refresh_token = models.CharField(max_length=1000, null=True)
    provider = models.CharField(max_length=32)
    email = models.EmailField()
    expiration_dt = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'provider', 'email')
        
        
class UserEmployerCandidate(models.Model):
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='candidate_key')
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
    ats_candidate_key = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('user', 'employer')
        
        
class UserApplicationReview(AuditFields, JobVynePermissionsMixin):
    # Keep in sync with ApplicationUtil
    class Rating(IntEnum):
        POSITIVE = 2
        NEUTRAL = 1
        NEGATIVE = 0
    
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='application_review')
    application = models.ForeignKey('JobApplication', on_delete=models.CASCADE, related_name='user_review')
    rating = models.SmallIntegerField()
    
    class Meta:
        unique_together = ('user', 'application')

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
        
        review_filter = Q(user_id=user.id)
        if user.is_employer:
            review_filter |= Q(application__employer_job__employer_id=user.employer_id)
    
        return query.filter(review_filter)

    def _jv_can_create(self, user):
        return any([
            user.id == self.application.social_link.owner_id,
            user.is_employer and (user.employer_id == self.application.employer_job.employer_id)
        ])
    
    
class UserEmployerPermissionGroup(models.Model):
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='employer_permission_group')
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
    permission_group = models.ForeignKey('EmployerAuthGroup', on_delete=models.CASCADE)
    is_employer_approved = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'employer', 'permission_group')
        

class UserUnknownEmployer(AuditFields):
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE)
    employer_name = models.CharField(max_length=100)
    
    
class UserEmployeeProfileResponse(models.Model):
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='profile_response')
    question = models.ForeignKey('UserEmployeeProfileQuestion', on_delete=models.CASCADE)
    answer = models.TextField()
    
    class Meta:
        unique_together = ('user', 'question')
    
    
class UserEmployeeProfileQuestion(models.Model):
    text = models.TextField()


class UserNotificationPreference(models.Model, JobVynePermissionsMixin):
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='notification_preference')
    notification_key = models.CharField(max_length=40)
    is_enabled = models.BooleanField()

    class Meta:
        unique_together = ('user', 'notification_key')

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
    
        return query.filter(user_id=user.id)
    
    def _jv_can_create(self, user):
        return self.user_id == user.id
    
    
class UserSocialSubscription(AuditFields):
    """Push content to user's social feed
    """
    class SubscriptionType(Enum):
        jobs = 'JOBS'  # Receive updates on any jobs
        events = 'EVENTS'
        news = 'NEWS'
        
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='social_subscription')
    provider = models.CharField(max_length=32)  # OauthProviders
    subscription_type = models.CharField(max_length=40)
    subscription_data = models.JSONField()
    
    class Meta:
        unique_together = ('user', 'provider', 'subscription_type')
        
        
class UserConnection(AuditFields, JobVynePermissionsMixin):
    owner = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='owner_connection')
    connection_user = models.ForeignKey('JobVyneUser', null=True, blank=True, on_delete=models.CASCADE, related_name='other_connection')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)
    linkedin_handle = models.CharField(max_length=100, null=True, blank=True)
    employer_raw = models.CharField(max_length=200, null=True, blank=True)
    employer = models.ForeignKey('Employer', on_delete=models.SET_NULL, null=True, related_name='connection')
    job_title = models.CharField(max_length=100, null=True, blank=True)
    profession = models.ForeignKey('Taxonomy', null=True, blank=True, on_delete=models.SET_NULL)
    
    def _jv_can_create(self, user):
        return user.id == self.owner_id
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['owner', 'connection_user', 'employer_raw'], condition=Q(connection_user__isnull=False), name='unique_user_connection'),
            UniqueConstraint(fields=['owner', 'first_name', 'last_name', 'employer_raw'], name='unique_user_connection_name'),
            UniqueConstraint(fields=['owner', 'email', 'employer_raw'], condition=Q(email__isnull=False), name='unique_user_connection_email'),
            UniqueConstraint(fields=['owner', 'linkedin_handle', 'employer_raw'], name='unique_user_connection_linkedin'),
        ]
    
    @property
    def full_name(self):
        return ' '.join([n for n in [self.first_name, self.last_name] if n])
