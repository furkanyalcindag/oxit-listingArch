from django.db import models

from listArch.services.general_methods import category_parent_show


class Category(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True, verbose_name='Kategori')
    url = models.CharField(max_length=120, null=True, blank=True)
    is_parent = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(category_parent_show(self))
