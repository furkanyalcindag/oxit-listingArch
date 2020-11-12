from django.db import models

from listArch.models.Service import Service


class ServiceDesc(models.Model):
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.CASCADE)
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Lang Kod')
    description = models.CharField(blank=True, null=True, verbose_name='Çeviri', max_length=250)
