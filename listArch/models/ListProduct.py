from django.db import models

from listArch.models.Product import Product
from listArch.models.List import List


class ListProduct(models.Model):
    list = models.ForeignKey(List, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.product.name, '-', self.list)
