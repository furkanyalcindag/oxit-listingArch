from django.db import models

from listArch.models.Blog import Blog


class BlogDesc(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name='İçerik Çevirisi')
    title_desc = models.CharField(null=True, blank=True, verbose_name='Başlık Çevirisi', max_length=250)
    lang_code = models.IntegerField(blank=True, null=True, verbose_name='Dil Kod')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%s' % self.blog.key
