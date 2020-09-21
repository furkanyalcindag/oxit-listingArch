from django.db import models

from listArch.models.Blog import Blog
from listArch.models.Product import Product
from listArch.models.Company import Company


class CompanyBlog(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.blog.key, '-', self.company.name)
