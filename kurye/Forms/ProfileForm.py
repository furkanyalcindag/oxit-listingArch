from django import forms
from django.forms import ModelForm

from kurye.models.Profile import Profile

CHOICES_WITH_BLANK = (
    ('', '--------'),

)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile

        fields = (
            'profileImage', 'address', 'mobilePhone', 'tc', 'city',
            'district', 'phone', 'neighborhood')
        widgets = {
            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'placeholder': 'Adres', 'rows': '4'}),
            'mobilePhone': forms.TextInput(
                attrs={'class': 'form-control ', 'type': 'text',
                       'data-inputmask': '"mask": "(999) 999-9999"'  "data-mask",
                       'required': 'required'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control ', 'type': 'text',
                       'data-inputmask': '"mask": "(999) 999-9999"'  'data-mask',}),

            'tc': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'T.C. Kimlik Numarası',
                       'maxlength': '11', 'minlength': '11', 'required': 'required'}),
            'city': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%; ', "onChange": 'ilceGetir()', 'required': 'required'}),
            'district': forms.Select(choices=CHOICES_WITH_BLANK,
                                     attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'id': 'ilce_id', "onChange": 'mahalleGetir()',
                                            'required': 'required'}),
            'neighborhood': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible ',
                       'style': 'width: 100%; ',
                       'placeholder': 'Mahalle', 'id': 'neighborhood_id', 'required': 'required'
                       }),

        }
