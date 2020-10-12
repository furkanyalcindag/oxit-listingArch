from django.db import models


class BusinessType(models.Model):
    type = models.CharField(max_length=250, verbose_name='tip adı', null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.id, '-', self.type)
