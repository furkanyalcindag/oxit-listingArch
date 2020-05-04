from django.contrib.auth.models import User
from django.db import models

from kurye.models import City


class Company(models.Model):

    companyName = models.CharField(max_length=11, null=False, blank=False, verbose_name='Firma Adı')
    taxName = models.CharField(max_length=11, null=False, blank=False, verbose_name='Vergi Dairesi')
    taxNumber = models.CharField(max_length=11, null=False, blank=False, verbose_name='Vergi Numarası')
    phone = models.CharField(max_length=11, null=False, blank=False, verbose_name='Sabit Telefon')
    address = models.TextField(blank=False, null=False, verbose_name='Adres')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False, blank=False,
                             verbose_name='İl')
    district = models.TextField(blank=False, null=False, verbose_name='İlçe')

    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%d %s %s %s' % (self.id, '-', self.user.first_name, self.user.last_name)
