from django.db import models


class File(models.Model):
    file = models.FileField(upload_to='dosyalar/', null=True, blank=True, verbose_name='Ürün Dosya',
                            default='logo1.png')
    file_title = models.TextField(null=True, blank=True, verbose_name='Dosya Adı')
    file_type = models.TextField(null=True, blank=True, verbose_name='Dosya Tipi')

    def __str__(self):
        return '%s %s %s' % (self.file_title, '-', self.file)
