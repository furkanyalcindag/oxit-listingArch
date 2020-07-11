from django.db import models

from listArch.models.OptionValue import OptionValue


class OptionValueDesc(models.Model):
    option_value = models.ForeignKey(OptionValue, on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='Seçenek Değeri')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Lang Kod')
    description = models.CharField(blank=True, null=True, verbose_name='Çeviri', max_length=250)

    def __str__(self):
        return '%s ' % self.description
