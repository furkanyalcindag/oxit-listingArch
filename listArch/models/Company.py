from django.contrib.auth.models import User
from django.db import models

from listArch.models.City import City
from listArch.models.Country import Country


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(blank=True, null=True, verbose_name='Firma Adı', max_length=250)
    file = models.FileField(upload_to='dosyalar/', null=True, blank=True, verbose_name='Sözleşme Dosya',
                            default='logo1.png',
                            )

    address = models.TextField(null=True, blank=True, verbose_name='Firma Adresi')
    phone = models.CharField(null=True, blank=True, verbose_name='Firma Telefonu', max_length=11)
    website = models.TextField(null=True, blank=True, verbose_name='Firma Web Adresi')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ülke')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Şehir')
    map = models.TextField(null=True, blank=True, verbose_name='Konum')
    description = models.TextField(null=True, blank=True, verbose_name='Açıklama')

    def __str__(self):
        return '%s %s %s' % (self.name, '-', self.phone)
