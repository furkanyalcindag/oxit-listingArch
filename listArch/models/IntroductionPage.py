from django.db import models

from listArch.models.IntroductionTitle import IntroductionTitle
from listArch.models.Category import Category


class IntroductionPage(models.Model):
    key = models.TextField(null=True, blank=True, verbose_name='Başlık')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    isActive = models.BooleanField(default=False)
    title = models.ForeignKey(IntroductionTitle, on_delete=models.CASCADE, null=True, blank=True)


