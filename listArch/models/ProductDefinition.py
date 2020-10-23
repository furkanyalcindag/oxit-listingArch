from django.db import models

from listArch.models.Definition import Definition
from listArch.models.Product import Product


class ProductDefinition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ürün')
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name='Açıklama')

    def __str__(self):
        return '%s %s %s' % (self.product.name, '-', self.definition)