from oxiterp.settings.base import *

# Override base.py settings here


DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'new2_oxit_kurye',
        'USER': 'postgres',
        'PASSWORD': 'oxit2016',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_ROOT = "/var/www/static/listArch"

STAICFILES_DIR = [

    "/var/www/static/listArch"

]

try:
    from oxiterp.settings.local import *
except:
    pass
