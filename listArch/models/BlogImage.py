from django.db import models

from listArch.models.Blog import Blog
from listArch.models.Image import Image


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s %s %s ' % (self.blog.key, '-', self.image.image)
