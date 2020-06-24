from django.db import models
from kurye.models.Profile import Profile
import uuid


class Company(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Firma Yetkilisi')
    companyName = models.CharField(max_length=250, null=False, blank=False, verbose_name='Firma Adı')
    taxName = models.CharField(max_length=250, null=False, blank=False, verbose_name='Vergi Dairesi')
    taxNumber = models.CharField(max_length=11, null=False, blank=False, verbose_name='Vergi Numarası')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True,
                                   verbose_name='İndirim Yüzdesi')

    def __str__(self):
        return '%d %s %s' % (self.id, '-', self.companyName)
