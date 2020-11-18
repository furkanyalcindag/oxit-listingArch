from django.db import models


class Blog(models.Model):
    key = models.TextField(null=True, blank=True, verbose_name='Blog İçeriği')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%s' % self.key
