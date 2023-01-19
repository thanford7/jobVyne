"""
Django settings for jobVyne project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import datetime
import json
import logging
import os
import sys
from pathlib import Path

from django.core.management.utils import get_random_secret_key
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default=get_random_secret_key())

DEBUG = env('DEBUG', cast=bool, default=False)
DEPLOY_TS = datetime.datetime.now()

PREPEND_WWW = False
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', default='127.0.0.1,localhost,0.0.0.0,backend').split(',')
PASSWORD_RESET_TIMEOUT = 60 * 60 * 8  # Reset is in seconds

IS_SEND_EMAILS = env('IS_SEND_EMAILS', cast=bool, default=True)
IS_LOCAL = env('IS_LOCAL', cast=bool)
if IS_LOCAL:
    CSRF_TRUSTED_ORIGINS = ['https://localhost']
else:
    CSRF_TRUSTED_ORIGINS = ['https://*.jobvyne.com']

SUBDOMAIN = env('SUBDOMAIN', default=None)
BASE_URL = 'https://localhost' if IS_LOCAL else (f'https://{SUBDOMAIN}.jobvyne.com' if SUBDOMAIN else 'https://jobvyne.com')
API_PATH = 'api/v1/'
API_URL = f'{BASE_URL}/{API_PATH}'

# Without this setting users will have different sign ins for different sub-domains (e.g. www.jobvyne.com vs jobvyne.com)
SESSION_COOKIE_DOMAIN = env('SESSION_COOKIE_DOMAIN', default=None)  # '.jobvyne.com'
IS_SEND_AUTO_POSTS = env('IS_SEND_AUTO_POSTS', cast=bool, default=False)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'jvapp',
    'django_extensions',
    'storages',
    'social_django',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'jobVyne.customMiddleware.AdminRedirectMiddleware',
    'jobVyne.customMiddleware.ErrorHandlerMiddleware'
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    # 'jobVyne.customSocialPipeline.redirect_if_no_refresh_token',
    'social_core.pipeline.social_auth.associate_by_email',
    'jobVyne.customSocialPipeline.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'jobVyne.customSocialPipeline.save_user_credentials',
)

AUTH_STATE = env('AUTH_STATE')
SOCIAL_AUTH_FACEBOOK_KEY = env('FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env('FACEBOOK_SECRET')
SOCIAL_AUTH_GOOGLE_KEY = env('GOOGLE_KEY')
SOCIAL_AUTH_GOOGLE_SECRET = env('GOOGLE_SECRET')
SOCIAL_AUTH_LINKEDIN_KEY = env('LINKEDIN_KEY')
SOCIAL_AUTH_LINKEDIN_SECRET = env('LINKEDIN_SECRET')

SOCIAL_AUTH_FACEBOOK_API_VERSION = '14.0'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, first_name, last_name, email, picture'
}
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['profile', 'email']
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    # https://python-social-auth.readthedocs.io/en/latest/use_cases.html#re-prompt-google-oauth2-users-to-refresh-the-refresh-token
    # 'approval_prompt': 'auto'
}
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_emailaddress', 'r_liteprofile', 'w_member_social']
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['emailAddress']
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    ('id', 'id'),
    ('firstName', 'first_name'),
    ('lastName', 'last_name'),
    ('emailAddress', 'email_address'),
    ('profilePicture', 'picture')
]

# this is needed to get a user's email from Facebook. See:
# https://stackoverflow.com/questions/32024327/facebook-doesnt-return-email-python-social-auth
# https://stackoverflow.com/a/32129851/6084948
# https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow/
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    "fields": "id,name,email",
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'jobVyne.multiPartJsonParser.MultiPartJsonParser',
        'rest_framework.parsers.FormParser'
    )
}

ROOT_URLCONF = 'jobVyne.urls'

FRONTEND_PORT = env('FRONTEND_PORT', default='9000')
if frontend_url_override := env('FRONTEND_URL_OVERRIDE', default=None):
    FRONTEND_URL = frontend_url_override
elif IS_LOCAL:
    FRONTEND_URL = 'https://localhost/'
else:
    FRONTEND_URL = 'https://jobvyne.com/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'jobVyne.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
db_config = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': env('MYSQL_DATABASE', default='jobvyne'),
    'HOST': env('MYSQL_DATABASE_HOST', default='db'),
    'PORT': env('MYSQL_DATABASE_PORT', default=3306),
}
if IS_LOCAL:
    db_config['USER'] = 'root'
    db_config['PASSWORD'] = env('MYSQL_ROOT_PASSWORD')
    DATABASES = {
        'default': db_config
    }
else:
    print('CURRENTLY IN PRODUCTION MODE')
    db_config['USER'] = env('MYSQL_USER', default='jobvyne')
    db_config['PASSWORD'] = env('MYSQL_PASSWORD')
    DATABASES = {
        'default': db_config
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'jvapp.JobVyneUser'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'jobVyne.passwordValidation.LowercaseCharValidator',
    },
    {
        'NAME': 'jobVyne.passwordValidation.UppercaseCharValidator',
    },
    {
        'NAME': 'jobVyne.passwordValidation.NumberValidator',
    },
    {
        'NAME': 'jobVyne.passwordValidation.SymbolValidator',
    },
    {
        'NAME': 'jobVyne.passwordValidation.WhitespaceValidator',
    },
]

# Email
ADMINS = [('Todd', 'todd@jobvyne.com')]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'  # Exactly that.
EMAIL_HOST_PASSWORD = env('SENDGRID_API_KEY')
EMAIL_PORT = 587  # 25 or 587 (for unencrypted/TLS connections).
EMAIL_USE_TLS = True
SERVER_EMAIL = 'no-reply@jobvyne.com'  # This is used to send error messages to admins
DEFAULT_FROM_EMAIL = 'no-reply@jobvyne.com'
SENDGRID_WEBHOOK_KEY = env('SENDGRID_WEBHOOK_KEY')

# SMS
TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN')

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = '/static/'
if IS_LOCAL:
    print('Using local static storage')
    STATIC_URL = '/static/'
    
    DEFAULT_FILE_STORAGE = 'jobVyne.customStorage.OverwriteStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    print('Using S3 static storage')
    AWS_QUERYSTRING_AUTH = False
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = 'jobvyne' if env('IS_PROD', default=False, cast=bool) else 'jobvyne-dev'
    AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_DEFAULT_ACL = 'public-read'
    AWS_IS_GZIPPED = True
    
    AWS_LOCATION = 'static-files'
    STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    # Media file storage
    DEFAULT_FILE_STORAGE = 'jobVyne.customStorage.MediaStorage'
    MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_ENDPOINT_URL}/{MEDIA_LOCATION}/'
    MEDIA_BASE = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/{MEDIA_LOCATION}/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOG_LEVEL = env('LOG_LEVEL', default=None) or 'DEBUG' if DEBUG else 'WARNING'
print(f'Log level: {LOG_LEVEL}')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'msg_only': {
            'format': '{message}',
            'style': '{',
        },
        'long': {
            'format': '{asctime} | {name} | {levelname} | {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} | {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'long'
        },
        'sql': {
            'class': 'logging.StreamHandler',
            # 'level': 'DEBUG',
            'formatter': 'msg_only',
            'filters': ['require_debug_true']
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'mail_admins'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'django.db.backends': {
            'level': LOG_LEVEL,
            'handlers': ['sql'],
            'propagate': False
        }
    }
}

# reCAPTCHA
GOOGLE_CAPTCHA_SITE_KEY = env('GOOGLE_CAPTCHA_SITE_KEY')
GOOGLE_PROJECT_ID = env('GOOGLE_PROJECT_ID')

# Set Google Env variable from string (needs to be a path to a file)
google_credentials = json.loads(env('GOOGLE_APPLICATION_CREDENTIALS_STR').replace('\'', '"'), strict=False)

os.makedirs(f'{BASE_DIR}/secure', exist_ok=True)
file_path = f'{BASE_DIR}/secure/google-captcha.json'
with open(file_path, 'w') as outfile:
    json.dump(google_credentials, outfile)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = file_path

# Geolocation
GEOIP_PATH = f'{BASE_DIR}/jvapp/geolocation'  # This is for location lookup of an IP address
GOOGLE_MAPS_KEY = env('GOOGLE_MAPS_KEY')  # This is for reverse geolocation lookup

# Stripe payments
IS_STRIPE_LIVE = env('IS_STRIPE_LIVE', cast=bool, default=False)
if IS_STRIPE_LIVE:
    STRIPE_PRIVATE_KEY = env('STRIPE_LIVE_PRIVATE_KEY')
    STRIPE_WEBHOOK_PRIVATE_KEY = env('STRIPE_LIVE_WEBHOOK_PRIVATE_KEY')
else:
    STRIPE_PRIVATE_KEY = env('STRIPE_PRIVATE_KEY')
    STRIPE_WEBHOOK_PRIVATE_KEY = env('STRIPE_WEBHOOK_PRIVATE_KEY')
    
# Lever
LEVER_SCOPE = ' '.join([
    'applications:read:admin',
    'notes:write:admin',
    'opportunities:write:admin',
    'postings:read:admin',
    'referrals:read:admin',
    'requisitions:read:admin',
    'requisition_fields:read:admin',
    'sources:read:admin',
    'stages:read:admin',
    'users:write:admin',
    'webhooks:write:admin',
    'offline_access'
])
LEVER_CALLBACK_URL = '/employer/employer-settings?tab=integration'
LEVER_CLIENT_ID = env('LEVER_CLIENT_ID')
LEVER_CLIENT_SECRET = env('LEVER_CLIENT_SECRET')
LEVER_STATE = env('LEVER_STATE')
if LEVER_DEBUG := env('LEVER_DEBUG', cast=bool, default=True):
    LEVER_BASE_URL = 'https://api.sandbox.lever.co/v1/'
    LEVER_REDIRECT_BASE = 'https://sandbox-lever.auth0.com/authorize'
    LEVER_AUTH_TOKEN_URL = 'https://sandbox-lever.auth0.com/oauth/token'
else:
    LEVER_BASE_URL = 'https://api.lever.co/v1/'
    LEVER_REDIRECT_BASE = 'https://auth.lever.co/authorize'
    LEVER_AUTH_TOKEN_URL = 'https://auth.lever.co/oauth/token'

# CELERY_BROKER_URL = 'pyamqp://rabbitmq:5672'
