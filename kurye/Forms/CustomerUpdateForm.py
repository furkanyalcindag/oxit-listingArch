from django import forms
from django.forms import ModelForm

from kurye.models.Customer import Customer

CHOICES_WITH_BLANK = (
    ('', '-------'),

)


class CustomerUpdateForm(ModelForm):
    class Meta:
        model = Customer

        fields = ('customer', 'address', 'phone', 'city', 'district', 'email', 'neighborhood',)
        widgets = {
            'customer': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Ad Soyad', 'rows': '2', 'required': 'required'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Email', 'rows': '2', 'required': 'required'}),
            'address': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Açık Adres', 'rows': '2', 'required': 'required'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Cep Telefonu', 'required': 'required'}),
            'city': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%; ', "onChange": 'ilceGetir()'}),
            'district': forms.Select(choices=CHOICES_WITH_BLANK,
                                     attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'id': 'ilce_id', "onChange": 'mahalleGetir()', }),
            'neighborhood': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible ',
                       'style': 'width: 100%; ',
                       'placeholder': 'Mahalle', 'id': 'neighborhood_id',
                       }),

        }
