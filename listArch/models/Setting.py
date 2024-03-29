from django.db import models


class Setting(models.Model):
    name = models.CharField(max_length=120, null=True)
    value = models.TextField(blank=True, null=True)
    isActive = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.name, '-', self.value)
