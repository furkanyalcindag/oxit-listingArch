from django.db import models
from listArch.models.Category import Category
from listArch.models.Company import Company


class Product(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='Ürün Adı')
    code = models.TextField(blank=True, null=True, verbose_name='Ürün Kodu')
    company_code = models.TextField(blank=True, null=True, verbose_name='Ürün Kodu')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Ürüne Ait Firma')
    isActive = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True,
                                verbose_name='Ürün Fiyatı')
    cover_image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Ürün Kapak Resmi')
    category = models.ManyToManyField(Category, null=True, blank=True)
    isSponsor = models.BooleanField(default=False)
    isAdvert = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s %s' % (self.name, '-', self.code)
