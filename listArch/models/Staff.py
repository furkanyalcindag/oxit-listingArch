from django.contrib.auth.models import User
from django.db import models


class Staff(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='Telefon')

