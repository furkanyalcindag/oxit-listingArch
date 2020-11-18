from django.db import models



class BusinessType(models.Model):
    key = models.CharField(max_length=250, verbose_name='tip adı', null=True, blank=True)
    isProduct_based = models.BooleanField(default=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%s' % self.key
