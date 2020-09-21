from django.db import models


class IntroductionTitle(models.Model):
    key = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.key