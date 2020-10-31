from django.db import models


class GraphicValue(models.Model):
    min = models.CharField(null=True, blank=True, verbose_name="Minimum Değer", max_length=250)
    max = models.CharField(null=True, blank=True, verbose_name="Maksimum Değer", max_length=250)
    middle = models.CharField(null=True, blank=True, verbose_name="Ara Değer", max_length=250)
    current_value = models.CharField(null=True, blank=True, verbose_name="Mevcut Değer", max_length=250)
    unit = models.CharField(null=True, blank=True, verbose_name="Grafik Birimi", max_length=250)

