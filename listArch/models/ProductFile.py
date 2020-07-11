from django.db import models

from listArch.models.Product import Product
from listArch.models.File import File


class ProductFile(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, verbose_name='Ürün Dosyası', on_delete=models.CASCADE)
    file = models.ForeignKey(File, null=True, blank=True, verbose_name='Ürün Dosyası', on_delete=models.CASCADE)
