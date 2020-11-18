from django.db import models

from listArch.models.Product import Product
from listArch.models.Category import Category


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ürün')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='Ürün Kategorisi')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')


def __str__(self):
        return '%s %s %s' % (self.product.name, '-', self.category.name)
