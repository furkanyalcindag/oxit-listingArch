from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Ürün Resmi',
                              )
    order = models.IntegerField(null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
