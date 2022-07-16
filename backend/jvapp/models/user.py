from enum import Enum

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import crypto, timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


__all__ = ('CustomUserManager', 'JobVyneUser')

from jvapp.models.abstract import JobVynePermissionsMixin


class PermissionName(Enum):
    MANAGE_USER = 'Manage users'
    CHANGE_PERMISSIONS = 'Change user permissions'
    MANAGE_PERMISSION_GROUPS = 'Manage custom permission groups'
    MANAGE_EMPLOYER_CONTENT = 'Manage employer content'
    MANAGE_EMPLOYER_JOBS = 'Manage employer jobs'
    MANAGE_REFERRAL_BONUSES = 'Manage employee referral bonuses'
    ADD_EMPLOYEE_CONTENT = 'Add personal employee content'
    MANAGE_BILLING_SETTINGS = 'Add personal employee content'
    

USER_MANAGEMENT_PERMISSIONS = [
    PermissionName.MANAGE_USER.value,
    PermissionName.CHANGE_PERMISSIONS.value,
]


class DefaultPermissionGroups(Enum):
    ADMIN = 'Admin'
    HR = 'HR Professional'
    EMPLOYEE = 'Employee'
    INFLUENCER = 'Influencer'


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password or generate_password())
        # TODO: If not password, send password reset email
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

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
    
    ALL_USER_TYPES = [
        USER_TYPE_ADMIN,
        USER_TYPE_CANDIDATE,
        USER_TYPE_EMPLOYEE,
        USER_TYPE_INFLUENCER,
        USER_TYPE_EMPLOYER
    ]
    
    username = None
    date_joined = None
    email = models.EmailField(_('email address'), unique=True)
    user_type_bits = models.SmallIntegerField()
    employer = models.ForeignKey('Employer', on_delete=models.SET_NULL, null=True, related_name='employee')
    is_employer_deactivated = models.BooleanField(default=False, blank=True)
    permission_groups = models.ManyToManyField('EmployerAuthGroup', related_name='user')
    created_dt = models.DateTimeField(_("date created"), default=timezone.now)
    modified_dt = models.DateTimeField(_("date modified"), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type_bits']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def has_employer_permission(self, permission_name: str or list, is_all_true: bool = True):
        """Check if user has the specified permission
        :param permission_name: A property of PermissionName class
        :param is_all_true: If true, all permissions must be true.
            Otherwise if one permission is true, the func will return true
        """
        if isinstance(permission_name, str):
            permission_name = [permission_name]
        check_method = all if is_all_true else any
        return check_method((self.permissions.get(p) for p in permission_name))
    
    def _jv_can_create(self, user):
        return user.is_admin or (
            user.has_employer_permission(PermissionName.MANAGE_USER.value)
            and self.employer_id == user.employer_id
        )
    
    def _jv_can_delete(self, user):
        return user.is_admin or self.id == user.id
        
    @cached_property
    def permissions(self):
        permission_groups = self.permission_groups.prefetch_related('permissions').all()
        return {permission.name: permission for group in permission_groups for permission in group.permissions.all()}
    
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


def generate_password():
    return crypto.get_random_string(length=30, allowed_chars=crypto.RANDOM_STRING_CHARS + '!@#$%^&*()-+=')
