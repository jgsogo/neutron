#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings for neutron project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from __future__ import unicode_literals

import os
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+hcs+p=cciojzmvujur=9rh8xwxk56#rht(q*3#vzze%$gafkj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost',]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap3',  # https://github.com/dyve/django-bootstrap3
    'mptt',
    'rosetta',  # http://django-rosetta.readthedocs.io/en/latest/installation.html

    'server',
    'neutron',
    'question.worduse',  # Game WordUse
    'question.wordcoarse',  # Game WordCoarse
    'question.wordalternate',  # Game WordAlternate
    'telegram',
    'synthetic',
    'exporter',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'server/templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es'
LANGUAGES = [
    ('es', _('Español (genérico)')),
    ('es-AR', _('Argentina')),
    ('es-BO', _('Bolivia')),
    ('es-CL', _('Chile')),
    ('es-CO', _('Colombia')),
    ('es-CR', _('Costa Rica')),
    ('es-CU', _('Cuba')),
    ('es-EC', _('Ecuador')),
    ('es-SV', _('El Salvador')),
    ('es-ES', _('España')),
    ('es-GT', _('Guatemala')),
    ('es-GQ', _('Guinea Ecuatorial')),
    ('es-HN', _('Honduras')),
    ('es-MX', _('México')),
    ('es-NI', _('Nicaragua')),
    ('es-PA', _('Panamá')),
    ('es-PY', _('Paraguay')),
    ('es-PE', _('Perú')),
    ('es-PR', _('Puerto Rico')),
    ('es-DO', _('República Dominicana')),
    ('es-UY', _('Uruguay')),
    ('es-VE', _('Venezuela')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "server/static"),
)


from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

NEUTRON_BOT_USERNAME = 'neutron_test_bot'


LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
            },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "file.log"),
            'formatter': 'simple'
            },
        },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
            },
        'telegram': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
            },
        'neutron': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
            },
        'question': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
            },
        'exporter': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
            },
        }
    }

if DEBUG:
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] += ['console']



from .secret import *
try:
    from .local_settings import *
except ImportError:
    pass
