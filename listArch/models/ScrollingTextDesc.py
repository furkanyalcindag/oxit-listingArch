from django.db import models

from listArch.models.ScrollingText import ScrollingText


class ScrollingTextDesc(models.Model):
    text = models.ForeignKey(ScrollingText, on_delete=models.CASCADE, null=True, blank=True)
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Lang Kod')
    description = models.CharField(blank=True, null=True, verbose_name='Çeviri', max_length=250)
    subTextDesc = models.CharField(blank=True, null=True, verbose_name='Alt Yazı', max_length=250)
