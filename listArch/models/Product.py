from django.db import models
from django.template.defaultfilters import slugify

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
    unit_rate = models.CharField(null=True, blank=True, verbose_name='Birim Oranı', max_length=11)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    uuid = models.UUIDField(editable=False, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True, verbose_name='Sayaç', default=0)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return '%s %s %s' % (self.name, '-', self.code)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
