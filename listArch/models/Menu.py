from django.db import models
from django.contrib.auth.models import Permission, Group


class Menu(models.Model):
    name = models.CharField(max_length=120, null=True)
    url = models.CharField(max_length=120, null=True, blank=True)
    permission = models.OneToOneField(Permission, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='MenuPermissionAdmin')
    is_parent = models.BooleanField(default=True)
    is_show = models.BooleanField(default=True)
    fa_icon = models.CharField(max_length=120, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True, verbose_name='grup', on_delete=models.CASCADE)
