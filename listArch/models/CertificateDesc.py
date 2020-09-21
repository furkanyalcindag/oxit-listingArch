from django.db import models
from listArch.models.Certificate import Certificate


class CertificateDesc(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, null=True, blank=True)
    desc = models.TextField(null=True, blank=True, verbose_name='Çeviri')
