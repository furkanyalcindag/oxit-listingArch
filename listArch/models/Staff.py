from django.contrib.auth.models import User
from django.db import models


class Staff(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='Telefon')
    isActive = models.BooleanField(default=True, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi',null=True,blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
