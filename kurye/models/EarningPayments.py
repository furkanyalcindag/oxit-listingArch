from django.db import models
from kurye.models.Profile import Profile


class EarningPayments(models.Model):
    courier = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Ödeme Alan', null=True,blank=True,)
    payedDate = models.TextField(blank=True, null=True)
    payed = models.BooleanField(default=False)
    earning_date = models.TextField(blank=True, null=True)
    paymentTotal = models.DecimalField(verbose_name='Ödeme Tutarı', max_digits=10, decimal_places=2)
    task_count = models.IntegerField(null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

