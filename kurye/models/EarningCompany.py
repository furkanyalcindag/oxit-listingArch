from django.db import models

from kurye.models.Profile import Profile


class EarningCompany(models.Model):
    company = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Ödeme Yapacak Kullanıcı', null=True,
                                blank=True,
                                related_name='profile_company')
    payedDate = models.TextField(blank=True, null=True)
    earning_date = models.TextField(blank=True, null=True)
    paymentTotal = models.DecimalField(verbose_name='Ödeme Tutarı', max_digits=10, decimal_places=2)
    task_count = models.IntegerField(null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

