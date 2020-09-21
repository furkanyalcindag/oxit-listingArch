from django.db import models

from listArch.models import Product
from listArch.models.IntroductionPage import IntroductionPage


class IntroductionProduct(models.Model):
    introduction = models.ForeignKey(IntroductionPage, null=True, blank=True, verbose_name='Başlık',
                                     on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)


