from django.db import models

from listArch.models.GraphicValue import GraphicValue
from listArch.models.Product import Product


class ProductPerform(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    graphValue = models.ForeignKey(GraphicValue, on_delete=models.CASCADE, null=True, blank=True)
