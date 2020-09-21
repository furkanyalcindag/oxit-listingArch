from django.db import models

from listArch.models.IntroductionPage import IntroductionPage


class IntroductionPageDesc(models.Model):
    introduction = models.ForeignKey(IntroductionPage, on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='tanıtım')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Lang Kod')
    description = models.CharField(blank=True, null=True, verbose_name='Çeviri', max_length=250)
