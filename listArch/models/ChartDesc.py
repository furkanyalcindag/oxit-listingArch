from django.db import models

from listArch.models.Chart import Chart


class ChartDesc(models.Model):
    chart = models.ForeignKey(Chart, max_length=250, null=True, blank=True, verbose_name='Yıl',
                              on_delete=models.CASCADE)
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name='Grafik Adı')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Dil Kod')
