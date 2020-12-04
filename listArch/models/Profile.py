from django.contrib.auth.models import User
from django.db import models

from listArch.models import Country, City, BusinessType, Category


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    website = models.TextField(null=True, blank=True, verbose_name='Website Adresi')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(null=True, blank=True, verbose_name=models.CASCADE)
    profile_name = models.ForeignKey(BusinessType, on_delete=models.CASCADE, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    phone = models.CharField(null=True, blank=True, verbose_name='Telefon', max_length=13)
    map = models.TextField(null=True, blank=True, verbose_name='Konum')
    image = models.ImageField(upload_to='profile_image/', null=True, blank=True, verbose_name='Resim',
                              default='logo1.png')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
