from io import BytesIO
import qrcode
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from listArch.models.File import File
from listArch.models.Category import Category
from listArch.models.Company import Company
import uuid


class Product(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='Ürün Adı')
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ürün Kodu')
    code2 = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ürün Sıra Kodu')
    code3 = models.CharField(max_length=100, null=True, blank=True)
    company_code = models.TextField(blank=True, null=True, verbose_name='Ürün Kodu')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='Ürüne Ait Firma')
    isActive = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='Ürün Fiyatı')
    cover_image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Ürün Kapak Resmi')
    category = models.ManyToManyField(Category, null=True, blank=True)
    isSponsor = models.BooleanField(default=False)
    isAdvert = models.BooleanField(default=False)
    unit_rate = models.CharField(null=True, blank=True, verbose_name='Birim Oranı', max_length=11)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=True)
    count = models.IntegerField(null=True, blank=True, verbose_name='Sayaç', default=0)
    slug = models.SlugField(null=True, unique=True)
    related_product = models.ManyToManyField('self', null=True, blank=True)
    file = models.ManyToManyField(File, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi', null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%s %s %s' % (self.name, '-', self.code)

    def slug_save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + '-' + str(self.code))
            super().save(*args, **kwargs)
        from PIL import Image, ImageDraw
        from django.core.files import File



        if not self.qr_code:
            path = reverse('listArch:urun-detay', args=(self.slug,))

            qr = self.qr_generate(path)
            self.qr_code.save(self.slug + '.png', BytesIO(qr), save=False)

            '''qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=1,
            )
            qr.add_data('%s%s' % (Site.objects.get_current().domain, path))
            qrcode_img =qr.make(fit=True)


            #qrcode_img = qrcode.make('%s%s' % (Site.objects.get_current().domain, path))


            canvas = Image.new('RGB', (400, 400), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            fname = f'qr_code-{self.slug}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()'''
            super().save(*args, **kwargs)

    @staticmethod
    def qr_generate(path):
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(path))
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        qrByte = BytesIO()
        img.save(qrByte)
        return qrByte.getvalue()