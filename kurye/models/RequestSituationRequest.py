from django.db import models
from django.utils import timezone

from kurye.models.Request import Request
from kurye.models.RequestSituations import RequestSituations


class RequestSituationRequest(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True, blank=True)
    request_situation = models.ForeignKey(RequestSituations, on_delete=models.CASCADE, null=True, blank=True)
    isActive = models.BooleanField(default=False)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%s ' % self.request_situation.name
