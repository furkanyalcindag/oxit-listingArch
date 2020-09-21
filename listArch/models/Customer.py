from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    isCompany = models.BooleanField(default=False)
    companyName = models.CharField(max_length=250, null=True, blank=True, verbose_name='Firma adı')
    companyPhone = models.CharField(max_length=11, null=True, blank=True, verbose_name='Firma Tel')
    companyMail = models.CharField(max_length=150, null=True, blank=True, verbose_name='Firma Email')
    companyAddress = models.TextField(null=True, blank=True, verbose_name='Firma Adres')

    def __str__(self):
        return '%s %s %s %s %s' % (self.user.first_name, ' ', self.user.last_name, '-', self.isCompany)
