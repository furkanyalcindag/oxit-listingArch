from django.db import models
from django.utils import timezone

from kurye.models.Task import Task
from kurye.models.TaskSituations import TaskSituations


class TaskSituationTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    task_situation = models.ForeignKey(TaskSituations, on_delete=models.CASCADE, null=True, blank=True)
    isActive = models.BooleanField(default=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%s ' % self.task_situation.name
