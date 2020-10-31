from django.db import models


class Contact(models.Model):
    phone = models.CharField(null=True, blank=True, verbose_name='Telefon', max_length=11)
    email = models.CharField(null=True, blank=True, verbose_name='email', max_length=250)
    isActive = models.BooleanField(default=False)

