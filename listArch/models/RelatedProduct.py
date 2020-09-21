from django.db import models
from listArch.models.Product import Product


class RelatedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Ürün', related_name='product')
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name='İlişkili Ürün', related_name='related_product')

    def __str__(self):
        return '%s %s %s' % (self.product.name, '~', self.related_product.name)
