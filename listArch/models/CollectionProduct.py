from django.db import models

from listArch.models import Product
from listArch.models.Collection import Collection


class CollectionProduct(models.Model):
    collection = models.ForeignKey(Collection, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
