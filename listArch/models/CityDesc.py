from django.db import models

from listArch.models.City import City


class CityDesc(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Şehir')
    city_desc = models.TextField(null=True, blank=True, verbose_name='Şehir Adı')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Dil Kod')
