"""
Django settings for oxiterp project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

from django.conf.locale.tr import formats as tr_formats

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j-hgr1ce(!9xi#aaffs%hm@(*(9sfv0shfi!*=md20woa3a23d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mathfilters',
    'rest_framework',
    'listArch',
    'accounts',

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

ROOT_URLCONF = 'oxiterp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'oxiterp/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',

                # "education.services.general_methods.append_privileges",
            ],
        },

    },
]

WSGI_APPLICATION = 'oxiterp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#  'default': {
#       'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
# }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oxiterp3',
        'USER': 'postgres',
        'PASSWORD': 'oxit2016',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'tr'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS = ('%d-%m-%Y', '%Y-%m-%d')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.com.tr'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'kayit@oxityazilim.com'
EMAIL_HOST_PASSWORD = 'oxit2016'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join('oxiterp/static'),)

LOGIN_REDIRECT_URL = '/patient'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
