from django.db import models

from listArch.models.Product import Product


class ProductDesc(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name='Ürün')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Lang Kod')
    description = models.CharField(blank=True, null=True, verbose_name='Seçenek Çeviri', max_length=250)

    def __str__(self):
        return '%s %s %s' % (self.product.name, '-', self.description)
