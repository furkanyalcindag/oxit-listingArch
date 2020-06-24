from django.db import models
from kurye.models.Request import Request
from kurye.models.Courier import Courier
import uuid


class Task(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True, blank=True)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Kurye Çalışanı')
    creationTime = models.TimeField(auto_now_add=True, null=True, blank=True, verbose_name='Çıkış zamanı')
    creationDate = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Çıkış Tarihi')
    deliveryTime = models.TimeField(null=True, blank=True, verbose_name='Teslim zamanı')
    deliveryDate = models.DateField(null=True, blank=True, verbose_name='Teslim Tarihi')
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name='Açıklama')
    isComplete = models.BooleanField(default=False)
    activeTask = ''
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)


    def __str__(self):
        return '%s %s %s' % (self.request.receiver.customer, '-', self.request.receiver.address)
