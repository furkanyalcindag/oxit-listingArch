from django.db import models

from listArch.models.Option import Option


class OptionDesc(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name='Seçenek Adı')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Lang Kod')
    description = models.CharField(blank=True, null=True, verbose_name='Seçenek Çeviri', max_length=250)

    def __str__(self):
        return '%s %s %s' % (self.option.key, '-', self.description)
