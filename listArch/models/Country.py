from django.db import models


class Country(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='Şehir')
    code = models.CharField(blank=True, null=True, verbose_name='Ülke Kodu', max_length=100)


    def __str__(self):
        return '%s ' % self.name
