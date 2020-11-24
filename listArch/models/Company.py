from django.contrib.auth.models import User
from django.db import models

from listArch.models.Service import Service
from listArch.models.BusinessType import BusinessType
from listArch.models.Country import Country
from listArch.models.City import City


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(blank=True, null=True, verbose_name='Firma Adı', max_length=250)
    logo = models.ImageField(upload_to='logo/', null=True, blank=True, verbose_name='Dosya', default='logo1.png')
    date = models.DateField(null=True, blank=True, verbose_name='Kuruluş Tarihi')
    address = models.TextField(null=True, blank=True, verbose_name='Firma Adresi')
    phone = models.CharField(null=True, blank=True, verbose_name='Firma Telefonu', max_length=10)
    website = models.TextField(null=True, blank=True, verbose_name='Firma Web Adresi')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ülke')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Şehir')
    map = models.TextField(null=True, blank=True, verbose_name='Konum')
    userDescription = models.TextField(null=True, blank=True, verbose_name='Kullanıcı Hikayesi')
    isSponsor = models.BooleanField(default=False)
    noOfEmployees = models.IntegerField(null=True, blank=True, verbose_name='Çalışan Sayısı')
    annualSales = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                      verbose_name='Yıllık Satış Tutarı')
    address_link = models.TextField(null=True, blank=True, verbose_name='Konum Linki')
    business_type = models.ForeignKey(BusinessType, null=True, blank=True, verbose_name='Firma Tipi',
                                      on_delete=models.SET_NULL)
    cover_image = models.ImageField(upload_to='company_image/', null=True, blank=True, verbose_name='Kapak Fotoğrafı',
                                    default='logo1.png')
    service = models.ManyToManyField(Service, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name="Ünvan")
    mobilePhone = models.CharField(null=True, blank=True, verbose_name='Firma Cep Telefonu', max_length=13)


    def __str__(self):
        return '%s %s %s %s' % (self.name, '-', self.user.first_name, self.user.last_name)
