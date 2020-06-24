from django.db import models
from kurye.models.Profile import Profile


class Log(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    content = models.TextField(null=True, blank=True, verbose_name='İçerik')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%d %s %s' % (self.id, '-', self.content)
