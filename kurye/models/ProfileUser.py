from django.contrib.auth.models import User
from django.db import models

from kurye.models import City
from kurye.models.Company import Company


class ProfileUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='User')
    profileImage = models.ImageField(upload_to='profile/', null=True, blank=True, default='profile/user.png',
                                     verbose_name='Profil Resmi')
    tc = models.CharField(max_length=11, null=False, blank=False, verbose_name='T.C. Kimlik Numarası')
    mobilePhone = models.CharField(max_length=11, null=False, blank=False, verbose_name='Cep Telefonu')
    phone = models.CharField(max_length=11, null=False, blank=False, verbose_name='Sabit Telefon')
    address = models.TextField(blank=False, null=False, verbose_name='Adres')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False, blank=False,
                             verbose_name='İl')
    district = models.TextField(blank=False, null=False, verbose_name='İlçe')
    isContract = models.BooleanField(default=False)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%d %s %s %s' % (self.id, '-', self.user.first_name, self.user.last_name)
