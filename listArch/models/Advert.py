from django.db import models


class Advert(models.Model):
    image = models.TextField(null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    description = models.TextField(null=True, blank=True, verbose_name='Açıklama')
