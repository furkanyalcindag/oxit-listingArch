from django.db import models

from listArch.models import GraphicValue


class GraphicValueDesc(models.Model):
    graphValue = models.ForeignKey(GraphicValue, null=True, blank=True, on_delete=models.CASCADE)
    description = models.CharField(null=True, blank=True, verbose_name="Grafik Adı", max_length=250)
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Dil Kod')
