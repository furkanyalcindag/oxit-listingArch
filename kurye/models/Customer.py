from django.db import models

from kurye.models.City import City
from kurye.models.Company import Company


class Customer(models.Model):
    customer = models.CharField(max_length=250, null=True, blank=True, verbose_name='Müşteri Ad Soyad')
    address = models.TextField(null=True, blank=True, verbose_name='Müşteri Adres')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='Müşteri Telefon')
    email = models.CharField(max_length=250, null=True, blank=True, verbose_name='Email')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name='İl')
    district = models.CharField(max_length=250, null=True, blank=True, verbose_name='İlçe')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.customer, '-', self.phone)
