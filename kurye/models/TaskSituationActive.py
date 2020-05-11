from django.db import models

from kurye.models.Task import Task


class TaskSituationActive(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    isActive = models.BooleanField(default=False)
