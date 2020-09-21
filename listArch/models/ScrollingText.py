from django.db import models


class ScrollingText(models.Model):
    key = models.TextField(null=True, blank=True)
    isActive = models.BooleanField()
