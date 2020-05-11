from django.db import models

from kurye.models.TaskSituations import TaskSituations
from kurye.models.Request import Request
from kurye.models.Courier import Courier


class Task(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True, blank=True)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Kurye Çalışanı')
    creationTime = models.TimeField(auto_now_add=True, null=True, blank=True, verbose_name='Çıkış zamanı')
    creationDate = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Çıkış Tarihi')
    deliveryTime = models.TimeField(null=True, blank=True, verbose_name='Teslim zamanı')
    deliveryDate = models.DateField(null=True, blank=True, verbose_name='Teslim Tarihi')
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name='Açıklama')
    task_situation = models.ManyToManyField(TaskSituations, verbose_name='Görev Durumu', null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.task_situation, '-', self.request.receiver.address)

    def latest_catch(self):
        if len(self.task_situation.all()) > 0:
            return self.task_situation.objects.last().name
        else:
            return 0
