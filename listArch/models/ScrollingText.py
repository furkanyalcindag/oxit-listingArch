from django.db import models


class ScrollingText(models.Model):
    key = models.TextField(null=True, blank=True)
    isActive = models.BooleanField()
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

