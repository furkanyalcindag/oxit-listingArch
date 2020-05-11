from django.db import models

from kurye.models.Company import Company
from kurye.models.Courier import Courier
from kurye.models.Customer import Customer
from kurye.models.RequestSituations import RequestSituations
from kurye.models.City import City


class Request(models.Model):
    TRANSFER = 'Kredi Kartı'
    EFT = 'Havale/EFT'
    PAYMENT_CHOICES = (

        (TRANSFER, 'Kredi Kartı'),
        (EFT, 'Havale/EFT')
    )

    receiver = models.ForeignKey(Customer, blank=True, on_delete=models.CASCADE, verbose_name='Alıcı')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', null=True, blank=True)
    district = models.TextField(blank=True, null=True, verbose_name='İlçe')
    payment_type = models.CharField(max_length=128, verbose_name='Ödeme Türü', choices=PAYMENT_CHOICES,
                                    default=TRANSFER)
    exitTime = models.TimeField(blank=True, verbose_name='Çıkış zamanı')
    exitDate = models.DateField(blank=True, verbose_name='Çıkış Tarihi')
    totalPrice = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=True,
                                     verbose_name='Ödenecek Tutar')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    description = models.TextField(null=True, blank=True, verbose_name='Kurye Açıklaması')
    request_situation = models.ManyToManyField(RequestSituations)
    isApprove = models.BooleanField(default=False, verbose_name='Onay')
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE,
                                verbose_name='Talep Eden Firma')

    def latest_catch(self):
        if len(self.request_situation.all()) > 0:
            return self.request_situation.last().name

            # return self.order_situations.get_queryset()[len(self.order_situations.get_queryset())-1].name
            # return self.order_situations.all().order_by('id')[len(self.order_situations.all())-1]
        else:
            return 0
