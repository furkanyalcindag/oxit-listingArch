from django.db import models


class Contact(models.Model):
    phone = models.CharField(null=True, blank=True, verbose_name='Telefon', max_length=11)
    email = models.CharField(null=True, blank=True, verbose_name='email', max_length=250)
    isActive = models.BooleanField(default=False)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

