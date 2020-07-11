from django.db import models

from listArch.models.Option import Option
from listArch.models.Product import Product


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ürün')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Ürün Seçeneği')

    def __str__(self):
        return '%s %s %s' % (self.product.name, '-', self.option.key)
