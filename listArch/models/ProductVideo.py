from django.db import models
from listArch.models.Product import Product
from listArch.models.Video import Video


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, verbose_name='Ürün', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.video.file_key
