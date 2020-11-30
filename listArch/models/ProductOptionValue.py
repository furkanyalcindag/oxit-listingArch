from django.db import models

from listArch.models.OptionValue import OptionValue
from listArch.models.Product import Product


class ProductOptionValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ürün')
    option_value = models.ForeignKey(OptionValue, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name='Ürün Seçenek Değeri')
    range_value = models.TextField(null=True, blank=True, verbose_name='Aralık Değeri')
    text_value = models.TextField(null=True, blank=True, verbose_name='Anahtar Kelimeler')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%s %s %s' % (self.product.name, '-', self.option_value.value)
