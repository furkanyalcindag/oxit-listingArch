from django.db import models

from listArch.models.Country import Country


class CountryDesc(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ülke')
    country_desc = models.TextField(null=True, blank=True, verbose_name='Ülke Adı')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Dil Kod')
