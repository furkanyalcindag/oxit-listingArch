from django.db import models
from listArch.models.Category import Category
from listArch.models.Product import Product
from listArch.models.Blog import Blog


class BlogProduct(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s %s %s ' % (self.blog.key, '-', self.product.name)
