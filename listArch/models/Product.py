from django.db import models


class Product(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='Ürün Adı')
    code = models.TextField(blank=True, null=True, verbose_name='Ürün Kodu')

    def __str__(self):
        return '%s %s %s' % (self.name, '-', self.code)
