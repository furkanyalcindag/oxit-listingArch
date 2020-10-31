from django.db import models


class Value(models.Model):
    year = models.CharField(max_length=250, null=True, blank=True, verbose_name='Yıl')
    value = models.CharField(max_length=250, null=True, blank=True, verbose_name='Değer')
