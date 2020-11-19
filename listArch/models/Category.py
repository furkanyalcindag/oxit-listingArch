from django.db import models
from django.template.defaultfilters import slugify

from listArch.services.general_methods import category_parent_show


class Category(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True, verbose_name='Kategori')
    url = models.CharField(max_length=120, null=True, blank=True)
    is_parent = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    isActive = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icon/', null=True, blank=True, verbose_name='Kategori İkon')
    isBasic = models.BooleanField(default=False)
    order = models.IntegerField(null=True, blank=True, verbose_name='kategori sıralaması')
    uuid = models.UUIDField(editable=False, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True, verbose_name='Sayaç', default=0)
    slug = models.SlugField(null=True, unique=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return str(category_parent_show(self))

    def slug_save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name+str(self.id))
        return super().save(*args, **kwargs)
