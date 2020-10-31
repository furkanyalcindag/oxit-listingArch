from django.db import models


class Chart(models.Model):

    key = models.CharField(max_length=250, null=True, blank=True)
