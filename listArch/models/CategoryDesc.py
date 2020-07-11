from django.db import models

from listArch.models.Category import Category


class CategoryDesc(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name='Kategori')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Lang Kod')
    description = models.CharField(blank=True, null=True, verbose_name='Seçenek Çeviri', max_length=250)

    def __str__(self):
        return '%s %s %s' % (self.category.name, '-', self.description)
