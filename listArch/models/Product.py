from django.db import models

from listArch.models.Company import Company


class Product(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='Ürün Adı')
    code = models.TextField(blank=True, null=True, verbose_name='Ürün Kodu')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Ürüne Ait Firma')

    def __str__(self):
        return '%s %s %s' % (self.name, '-', self.code)
