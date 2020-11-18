from django.db import models

from listArch.models import Company


class Collection(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name='Koleksiyon Adı')
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
