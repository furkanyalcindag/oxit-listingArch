from django.db import models

from listArch.models.Option import Option


class OptionValue(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Özellik')
    value = models.TextField(blank=True, null=True, verbose_name='Seçenek Değer Adı')
    min = models.IntegerField(blank=True, null=True, verbose_name='min değer')
    max = models.IntegerField(blank=True, null=True, verbose_name='max değer')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%s' % self.value
