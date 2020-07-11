from django.db import models

from listArch.models.Product import Product
from listArch.models.Image import Image


class ProductImage(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
