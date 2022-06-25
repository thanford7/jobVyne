"""
Django settings for jobVyne project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import logging
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.core.management.utils import get_random_secret_key
from environ import environ

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
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost,0.0.0.0').split(',')

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
    'corsheaders',
    # 'storages',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'jobVyne.multiPartJsonParser.MultiPartJsonParser',
    ]
}

ROOT_URLCONF = 'jobVyne.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jobVyne.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
if IS_LOCAL := env('IS_LOCAL', cast=bool, default=False):
    logger.info('Local mode')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('LOCAL_DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': 'localhost',
            'PORT': 5432
        }
    }
else:
    logger.info('PRODUCTION MODE')


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'jvapp.JobVineUser'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SQL Logging
if env('SQL_LOG', cast=bool, default=False):
    LOGGING = {
        'version': 1,
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
            }
        }
    }

# CORS
CORS_ALLOW_CREDENTIALS = True
if IS_LOCAL:
    CORS_ALLOWED_ORIGINS = ('http://localhost:9100',)
    CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
else:
    CORS_ALLOWED_ORIGIN_REGEXES = (r'^https://\w+\.jobvyne\.com$',)
    CSRF_TRUSTED_ORIGINS = ('https://*.jobvyne.com',)
