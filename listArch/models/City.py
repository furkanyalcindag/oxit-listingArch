from django.db import models

from listArch.models.Country import Country


class City(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='Şehir')
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s ' % self.name
