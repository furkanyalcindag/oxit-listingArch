from django.db import models

from listArch.models.File import File


class FileDesc(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Dosya')
    file_title = models.TextField(null=True, blank=True, verbose_name='Dosya Adı')
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Dil Kod')
