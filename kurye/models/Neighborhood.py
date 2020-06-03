from django.db import models

from kurye.models.City import City
from kurye.models.District import District


class Neighborhood(models.Model):
    neighborhood_name = models.TextField(blank=True, null=True, verbose_name='Mahalle Adı')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.TextField(blank=True, null=True, verbose_name='İlçe')
    price = models.DecimalField(verbose_name='Fiyat', max_digits=10, decimal_places=2)

    def __str__(self):
        return '%s ' % self.neighborhood_name
