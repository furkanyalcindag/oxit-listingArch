from django.db import models

from listArch.models.Category import Category
from listArch.models.Company import Company


class File(models.Model):
    file = models.FileField(upload_to='dosyalar/', null=True, blank=True, verbose_name='Ürün Dosya',
                            default='logo1.png')
    file_title = models.TextField(null=True, blank=True, verbose_name='Dosya Adı')
    file_type = models.TextField(null=True, blank=True, verbose_name='Dosya Tipi')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.file_title, '-', self.file)
