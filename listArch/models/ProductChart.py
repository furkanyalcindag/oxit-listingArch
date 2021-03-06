from django.db import models

from listArch.models import Product
from listArch.models.Chart import Chart


class ProductChart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

