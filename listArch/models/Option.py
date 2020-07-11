from django.db import models

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

    def __str__(self):
        return '%s %s %s' % (self.key, '-', self.type)
