from django.db import models

from listArch.models.Category import Category

OPTION1 = 'Seçim'
OPTION3 = 'Onay Kutusu'
OPTION4 = 'Number'
OPTION5 = 'Range'

OPTION_CHOICES = (
    (OPTION1, 'Seçim'),
    (OPTION3, 'Onay Kutusu'),
    (OPTION4, 'Sayı'),
    (OPTION5, 'Değer Aralığı'),

)


class Option(models.Model):
    key = models.TextField(blank=True, null=True, verbose_name='Özellik')
    type = models.TextField(choices=OPTION_CHOICES, default=OPTION1, blank=True, null=True, verbose_name='Tip')
    isBasic = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')


    def __str__(self):
        return '%s %s %s' % (self.key, '-', self.type)
