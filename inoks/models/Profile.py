from django.contrib.auth.models import User
from django.db import models
from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField

from inoks.models import City, Job, District


class Profile(models.Model):
    MALE = 'Erkek'
    FEMALE = 'Kadın'
    UNKNOWN = 'Belirtmek İstemiyorum'

    ilkokul = 'İlkokul'
    lise = 'Lise'
    lisans = 'Lisans'
    master = 'Yüksek Lisans'
    pre = 'Önlisans'

    GENDER_CHOICES = (

        (MALE, 'Erkek'),
        (FEMALE, 'Kadın'),
        (UNKNOWN, 'Belirtmek İstemiyorum')
    )

    SCHOOL_CHOICES = (

        (ilkokul, 'İlkokul'),
        (lise, 'Lise'),
        (lisans, 'Lisans'),
        (master, 'Yüksek Lisans'),
        (pre, 'Önlisans'),

    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileImage = models.ImageField(upload_to='profile/', null=True, blank=True, default='profile/user.png',
                                     verbose_name='Profil Resmi')
    tc = models.CharField(max_length=11, null=False, blank=False, verbose_name='T.C. Kimlik Numarası')
    birthDate = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    mobilePhone = models.CharField(max_length=11, null=False, blank=False, verbose_name='Telefon Numarası')
    address = models.TextField(blank=False, null=False, verbose_name='Adres')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    gender = models.CharField(max_length=128, null=False, blank=False, verbose_name='Cinsiyeti', choices=GENDER_CHOICES,
                              default=MALE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False, blank=False,
                             verbose_name='İl')
    district = models.TextField(blank=False, null=False, verbose_name='İlçe')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Meslek')
    educationLevel = models.CharField(max_length=128, null=False, blank=False, verbose_name="Eğitim Düzeyi",
                                      choices=SCHOOL_CHOICES,
                                      default=ilkokul)
    sponsor = models.ForeignKey("Profile", on_delete=models.CASCADE, verbose_name='Sponsor', null=True, blank=True,
                                related_name='sp')
    isApprove = models.BooleanField(default=False, null=False, blank=False)
    isActive = models.BooleanField(default=False)
    isContract = models.BooleanField(default=False)
    activePassiveDate = models.DateTimeField(null=True, blank=True)
    iban = models.TextField(blank=True, null=True, verbose_name='iban')
    ibanAdSoyad = models.TextField(blank=True, null=True, verbose_name='ibanAdSoyad')

    def __str__(self):
        return '%d %s %s %s' % (self.id, '-', self.user.first_name, self.user.last_name)
