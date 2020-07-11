from django.db import models

from listArch.models.SocialMedia import SocialMedia
from listArch.models.Company import Company


class CompanySocialAccount(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    social_account = models.ForeignKey(SocialMedia, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.company.name, '-', self.social_account)
