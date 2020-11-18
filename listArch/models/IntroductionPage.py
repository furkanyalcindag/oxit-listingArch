from django.db import models

from listArch.models.Product import Product
from listArch.models.IntroductionTitle import IntroductionTitle
from listArch.models.Category import Category


class IntroductionPage(models.Model):
    key = models.TextField(null=True, blank=True, verbose_name='Başlık')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    isActive = models.BooleanField(default=False)
    title = models.ForeignKey(IntroductionTitle, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Product, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

