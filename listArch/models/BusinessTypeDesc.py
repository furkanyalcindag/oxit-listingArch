from django.db import models

from listArch.models import BusinessType


class BusinessTypeDesc(models.Model):
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name='Profil adı')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Dil Kod')
    description = models.TextField(blank=True, null=True, verbose_name='Kategori Çeviri')

    def __str__(self):
        return '%s %s %s' % (self.business_type.key, '-', self.description)
