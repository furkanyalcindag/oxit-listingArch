from django.db import models

from listArch.models import Company


class Collection(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name='Koleksiyon Adı')
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
