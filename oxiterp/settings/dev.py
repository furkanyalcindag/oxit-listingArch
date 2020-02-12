from oxiterp.settings.base import *

# Override base.py settings here


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mutek_son',
        'USER': 'postgres',
        'PASSWORD': 'oxit2016',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oxit_inoks',
        'USER': 'postgres',
        'PASSWORD': 'oxit2016',
        'HOST': '185.122.203.112',
        'PORT': '5432',
    }
}"""

#
#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.postgresql',
   #     'NAME': 'oxit_inoks',
    #    'USER': 'postgres',
     #   'PASSWORD': 'oxit2016',
      #  'HOST': '185.122.203.112',
       # 'PORT': '5432',
    #}
#}



try:
    from oxiterp.settings.local import *
except :
    pass
