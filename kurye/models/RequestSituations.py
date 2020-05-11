from django.db import models


class RequestSituations(models.Model):
    name = models.TextField(max_length=18500, blank=True, null=True, verbose_name='Talep Durumları')

    def __str__(self):
        return '%s ' % self.name
