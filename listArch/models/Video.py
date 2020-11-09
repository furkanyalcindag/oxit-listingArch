from django.db import models


class Video(models.Model):
    file = models.FileField(upload_to='product-video/', null=True, blank=True, verbose_name='Ürün Video')
    file_key = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.file)
