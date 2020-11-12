from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    list_name = models.TextField(null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi',null=True,blank=True)
    description = models.TextField(null=True, blank=True, verbose_name='açıklama')
    reference_list = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return '%d %s %s' % (self.id, '-', self.list_name)
