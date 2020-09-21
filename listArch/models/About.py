from django.db import models


class About(models.Model):
    key = models.TextField(null=True, blank=True)
    isActive = models.BooleanField(null=True, blank=True, default=True)

    def __str__(self):
        return '%s' % self.key
