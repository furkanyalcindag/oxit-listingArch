from django.db import models


class Service(models.Model):
    key = models.CharField(max_length=100, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')


def __str__(self):
        return self.key
