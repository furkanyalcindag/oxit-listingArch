from django.db import models


class File(models.Model):
    file = models.FileField(upload_to='dosyalar/', null=True, blank=True, verbose_name='Ürün Dosya',
                            default='logo1.png')
