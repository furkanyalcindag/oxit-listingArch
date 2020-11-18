from django import forms
from django.forms import ModelForm

from listArch.models.CompanyBlog import CompanyBlog

CHOICES_WITH_BLANK = (
    ('', '--------'),

)


class CompanyBlogForm(ModelForm):
    class Meta:
        model = CompanyBlog
        fields = ('company', 'product')
        widgets = {

            'product': forms.Select(choices=CHOICES_WITH_BLANK,
                                    attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%; ', 'id': 'product_id', 'name': 'product_id',
                                           'required': 'required'}),

            'company': forms.Select(choices=CHOICES_WITH_BLANK,
                                    attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;', "onChange": 'urunGetir()'}),
        }
