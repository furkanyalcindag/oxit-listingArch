from django.db import models

from listArch.models.Definition import Definition


class DefinitionDescription(models.Model):
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Açıklama')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Lang Kod')
    title_desc = models.TextField(null=True, blank=True, verbose_name='Açıklama Başlık Çevirisi')
    description = models.TextField(blank=True, null=True, verbose_name='Açıklama Çeviri')

    def __str__(self):
        return '%s %s %s' % (self.definition.key, '-', self.lang_code)
