from django.db import models

from listArch.models import Company
from listArch.models.Blog import Blog


class BlogCompany(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
