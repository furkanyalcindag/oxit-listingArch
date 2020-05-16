from django.db import models


class TaskSituations(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name='Görev Durumu')
    isVisibility = models.BooleanField(default=True, verbose_name='Kimler görebilir')

    def __str__(self):
        return '%s ' % self.name
