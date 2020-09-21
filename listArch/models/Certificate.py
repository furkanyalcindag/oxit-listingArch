from django.db import models


class Certificate(models.Model):
    key = models.TextField(null=True, blank=True, verbose_name='Sertifika Adı')
    certificate_file = models.FileField(upload_to='company_certificate/', null=True, blank=True,
                                        verbose_name='Firma Sertifika Dosyası',
                                        default='logo1.png')
