from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Ürün Resmi',
                              default='logo1.png')
    order = models.IntegerField(null=True, blank=True)
