from django.db import models

from listArch.models.HeaderText import HeaderText


class HeaderTextDesc(models.Model):
    headerText = models.ForeignKey(HeaderText, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name='İçerik Çevirisi')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Dil Kod')

    def __str__(self):
        return '%s' % self.headerText.key
