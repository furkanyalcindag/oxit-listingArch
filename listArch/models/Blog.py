from django.db import models


class Blog(models.Model):
    key = models.TextField(null=True, blank=True, verbose_name='Blog İçeriği')

    def __str__(self):
        return '%s' % self.key
