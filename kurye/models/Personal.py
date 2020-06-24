from django.db import models
from kurye.models.Company import Company
from kurye.models.Profile import Profile
import uuid


class Personal(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)



    def __str__(self):
        return '%s %s %s' % (self.profile.user.first_name, ' ', self.profile.user.last_name)
