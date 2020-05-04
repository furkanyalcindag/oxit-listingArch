"""
WSGI config for oxiterp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application


sys.path.append('/opt/django-ox/apps/django/django_projects/oxit-kurye')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oxiterp.settings.prod')

application = get_wsgi_application()
