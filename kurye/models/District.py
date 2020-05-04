from django.db import models

from kurye.models import City


class District(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='İlçe')
    city = models.ForeignKey(City,on_delete=models.CASCADE)

    def __str__(self):
        return '%s ' % self.name
