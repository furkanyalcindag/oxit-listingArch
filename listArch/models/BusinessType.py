from django.db import models


class BusinessType(models.Model):
    key = models.CharField(max_length=250, verbose_name='tip adı', null=True, blank=True)
    isProduct_based = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % (self.key)
