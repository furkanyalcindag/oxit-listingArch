from django.db import models


class SocialMedia(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='Sosyal Medya')
    link = models.TextField(blank=True, null=True, verbose_name='Sosyal Medya Hesabı')

    def __str__(self):
        return '%s %s %s' % (self.link, '-', self.name)
