from oxiterp.settings.base import *

# Override base.py settings here


DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lofr',
        'USER': 'oxitowner',
        'PASSWORD': 'oxit2016',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_ROOT = "/var/www/staticList/listArch"

STAICFILES_DIR = [

    "/var/www/staticList/listArch"

]

try:
    from oxiterp.settings.local import *
except:
    pass
