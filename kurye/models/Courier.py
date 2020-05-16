from django.db import models

from kurye.models.Profile import Profile


class Courier(models.Model):
    courier = models.ForeignKey(Profile, max_length=250, null=True, blank=True, verbose_name='Kurye',
                                on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s %s %s' % (self.courier.user.first_name, self.courier.user.last_name, '-',
                                self.courier.mobilePhone)
