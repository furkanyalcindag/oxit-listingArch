from django.db import models


class HeaderText(models.Model):
    key = models.TextField(null=True, blank=True, verbose_name='Blog İçeriği')
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s %s' % (self.key, '-', self.isActive)
