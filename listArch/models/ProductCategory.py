from django.db import models

from listArch.models.Product import Product
from listArch.models.Category import Category


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ürün')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='Ürün Kategorisi')

    def __str__(self):
        return '%s %s %s' % (self.product.name, '-', self.category.name)
