from django import forms
from django.forms import ModelForm

from kurye.models import Neighborhood

CHOICES_WITH_BLANK = (
    ('', '--------'),

)


class NeighborhoodUpdateForm(ModelForm):
    class Meta:
        model = Neighborhood

        fields = (
            'city', 'district', 'neighborhood_name', 'price')
        widgets = {

            'city': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%; ', "onChange": 'ilceGetir()'}),
            'district': forms.Select(choices=CHOICES_WITH_BLANK,
                                     attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'id': 'ilce_id',"onChange": 'mahalleGetir()',}),
            'neighborhood_name': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible ',
                       'style': 'width: 100%; ',
                       'placeholder': 'Mahalle', 'id': 'neighborhood_id',
                       }),
            'price': forms.NumberInput(
                attrs={'class': 'form-control ', 'placeholder': 'Mahalleye göre fiyat (₺)',
                       }),

        }
