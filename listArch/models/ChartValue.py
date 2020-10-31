from django.db import models

from listArch.models.Chart import Chart
from listArch.models.Value import Value


class ChartValue(models.Model):
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, null=True, blank=True)
    value = models.ForeignKey(Value, on_delete=models.CASCADE, null=True, blank=True)
