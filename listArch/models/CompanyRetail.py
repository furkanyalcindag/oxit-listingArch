from django.db import models

from listArch.models import Company


class CompanyRetail(models.Model):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(blank=True, null=True, verbose_name='Firma Adı', max_length=250)
    logo = models.ImageField(upload_to='retail/', null=True, blank=True, verbose_name='Dosya', default='logo1.png')
    isCompany = models.BooleanField(default=False, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
