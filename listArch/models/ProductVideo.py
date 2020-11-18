from django.db import models
from listArch.models.Product import Product
from listArch.models.Video import Video


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, verbose_name='Ürün', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, null=True, blank=True, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')


def __str__(self):
        return '%s' % self.video.file_key
