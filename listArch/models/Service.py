from django.db import models


class Service(models.Model):
    key = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.key
