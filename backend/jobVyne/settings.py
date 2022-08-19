"""
Django settings for jobVyne project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import json
import logging
import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
import environ

from jvapp.utils.logger import setLogger

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default=get_random_secret_key())

DEBUG = env('DEBUG', cast=bool, default=False)

LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logger = setLogger(LOG_LEVEL)
logger.info(f'Base directory is: {BASE_DIR}')

PREPEND_WWW = False
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', default='127.0.0.1,localhost,0.0.0.0').split(',')
PASSWORD_RESET_TIMEOUT = 60 * 60 * 8  # Reset is in seconds

IS_LOCAL = env('IS_LOCAL', cast=bool)
if IS_LOCAL:
    CSRF_TRUSTED_ORIGINS = ['https://localhost']
else:
    CSRF_TRUSTED_ORIGINS = ['https://*.jobvyne.com']

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
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
    # 'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'jobVyne.customSocialPipeline.create_user',
    # 'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
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
        'jobVyne.multiPartJsonParser.MultiPartJsonParser',
    )
}

ROOT_URLCONF = 'jobVyne.urls'

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
    logger.info('CURRENTLY IN PRODUCTION MODE')
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
SENDGRID_API_KEY = env('SENDGRID_API_KEY')
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'  # Exactly that.
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587  # 25 or 587 (for unencrypted/TLS connections).
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'no-reply@jobvyne.com'

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
    logger.info('Using local static storage')
    STATIC_URL = '/static/'
    
    DEFAULT_FILE_STORAGE = 'jobVyne.customStorage.OverwriteStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    logger.info('Using S3 static storage')
    AWS_QUERYSTRING_AUTH = False
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = 'jobvyne'
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

# SQL Logging
if env('SQL_LOG', cast=bool, default=None):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
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
GEOIP_PATH = f'{BASE_DIR}/jvapp/geolocation'
