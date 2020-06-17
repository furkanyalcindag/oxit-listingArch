from django.contrib.auth.models import User
from django.db import models

from kurye.models.Profile import Profile


class Notification(models.Model):
    key = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField(verbose_name='Bildirim İçeriği', null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    isRead = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s %s' % (self.key, '-', self.message,)