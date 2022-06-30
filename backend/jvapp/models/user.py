from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import crypto, timezone
from django.utils.translation import gettext_lazy as _


__all__ = ('CustomUserManager', 'JobVineUser',)


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


class JobVineUser(AbstractUser):
    USER_TYPE_ADMIN = 0x1
    USER_TYPE_CANDIDATE = 0x2
    USER_TYPE_INFLUENCER = 0x4
    USER_TYPE_EMPLOYER = 0x8

    username = None
    date_joined = None
    email = models.EmailField(_('email address'), unique=True)
    user_type_bits = models.SmallIntegerField()
    created_dt = models.DateTimeField(_("date created"), default=timezone.now)
    modified_dt = models.DateTimeField(_("date modified"), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type_bits']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


def generate_password():
    return crypto.get_random_string(length=30, allowed_chars=crypto.RANDOM_STRING_CHARS + '!@#$%^&*()-+=')
