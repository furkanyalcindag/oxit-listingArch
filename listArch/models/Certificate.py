from django.db import models


class Certificate(models.Model):
    key = models.TextField(null=True, blank=True, verbose_name='Sertifika Adı')
    certificate_file = models.FileField(upload_to='company_certificate/', null=True, blank=True,
                                        verbose_name='Firma Sertifika Dosyası',
                                        default='logo1.png')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
