from django.db import models

from listArch.models.Category import Category


class CategoryDesc(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name='Kategori')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Dil Kod')
    description = models.TextField(blank=True, null=True, verbose_name='Kategori Çeviri')
    definition = models.TextField(blank=True, null=True, verbose_name='Açıklama Çevirisi')

    def __str__(self):
        return '%s %s %s' % (self.category.name, '-', self.description)
