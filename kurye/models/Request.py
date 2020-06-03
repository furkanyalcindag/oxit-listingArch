from django.db import models

from kurye.models.Company import Company
from kurye.models.Customer import Customer
from kurye.models.City import City
from kurye.models.Neighborhood import Neighborhood


class Request(models.Model):
    TRANSFER = 'Kredi Kartı'
    NAKIT = 'Nakit'
    MULTINET = 'Mutinet'
    SODEXO = 'Sodexo'
    TICKET = 'Ticket'
    RESTONET = 'Restonet'
    PAYMENT_CHOICES = (

        (TRANSFER, 'Kredi Kartı'),
        (NAKIT, 'Nakit'),
        (MULTINET, 'Mutinet'),
        (SODEXO, 'Sodexo'),
        (TICKET, 'Ticket'),
        (RESTONET, 'Restonet')
    )

    receiver = models.ForeignKey(Customer, blank=True, on_delete=models.CASCADE, verbose_name='Alıcı')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', null=True, blank=True)
    district = models.TextField(blank=True, null=True, verbose_name='İlçe')
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, verbose_name='Mahalle', null=True,
                                     blank=True)
    payment_type = models.CharField(max_length=128, verbose_name='Ödeme Türü', choices=PAYMENT_CHOICES,
                                    default=NAKIT)
    exitTime = models.TimeField(blank=True, verbose_name='Çıkış zamanı')
    exitDate = models.DateField(blank=True, verbose_name='Çıkış Tarihi')
    totalPrice = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=True,
                                     verbose_name='Sipariş Tutarı')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    description = models.TextField(null=True, blank=True, verbose_name='Kurye Açıklaması')

    isApprove = models.BooleanField(default=True, null=True, blank=True,
                                    verbose_name='Onay')
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE,
                                verbose_name='Talep Eden Firma')
    request_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=True,
                                        verbose_name='Talep Tutarı')
    isPayed = models.BooleanField(default=False)
    payedDate = models.TextField(null=True, blank=True, verbose_name='Ödeme Tarihi')

    def __str__(self):
        return '%s %s %s %s %s' % (self.company.companyName, '-', self.exitDate, '-', self.exitTime)
