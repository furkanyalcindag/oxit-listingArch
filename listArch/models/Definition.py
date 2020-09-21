from django.db import models


class Definition(models.Model):
    key = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s' % self.key
