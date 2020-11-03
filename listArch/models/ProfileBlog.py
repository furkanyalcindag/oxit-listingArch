from django.db import models

from listArch.models.Profile import Profile
from listArch.models.Blog import Blog


class ProfileBlog(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
