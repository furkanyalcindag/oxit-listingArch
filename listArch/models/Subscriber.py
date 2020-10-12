from datetime import datetime
from django.db import models


class Subscriber(models.Model):
    email = models.CharField(max_length=150, null=True, blank=True, verbose_name='Abone Email')
    creationDate = models.DateTimeField(verbose_name='Kayıt Tarihi', default=datetime.now())
    isActive = models.BooleanField(default=False)

