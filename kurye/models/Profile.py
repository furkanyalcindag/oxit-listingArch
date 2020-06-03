from django.contrib.auth.models import User
from django.db import models

from kurye.models.Neighborhood import Neighborhood
from kurye.models.City import City


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileImage = models.ImageField(upload_to='profile/', null=True, blank=True, default='profile/user.png',
                                     verbose_name='Profil Resmi')
    tc = models.CharField(max_length=11, null=True, blank=True, verbose_name='T.C. Kimlik Numarası')
    mobilePhone = models.CharField(max_length=11, null=False, blank=False, verbose_name='Cep Telefonu')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='Sabit Telefon')
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='İl')
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, verbose_name='Mahalle', null=True,
                                    blank=True)
    birthDate = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    district = models.TextField(blank=True, null=True, verbose_name='İlçe')
    isContract = models.BooleanField(default=False)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    isActive = models.BooleanField(default=False, verbose_name='Aktif/Pasif')

    def __str__(self):
        return '%s %s %s %s' % (self.mobilePhone, '-', self.user.first_name, self.user.last_name)
