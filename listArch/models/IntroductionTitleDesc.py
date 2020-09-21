from django.db import models

from listArch.models.IntroductionTitle import IntroductionTitle


class IntroductionTitleDesc(models.Model):
    title = models.ForeignKey(IntroductionTitle, on_delete=models.CASCADE, null=True, blank=True)
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Lang Kod')
    description = models.CharField(blank=True, null=True, verbose_name='Çeviri', max_length=250)
