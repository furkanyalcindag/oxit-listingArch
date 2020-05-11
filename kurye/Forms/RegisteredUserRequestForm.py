from django import forms
from django.forms import ModelForm

from kurye.models.Request import Request

CHOICES_WITH_BLANK = (
    ('', '--------'),

)


class RegisteredUserRequestForm(ModelForm):
    class Meta:
        model = Request

        fields = (
            'receiver', 'city', 'district', 'exitTime', 'exitDate', 'totalPrice',
            'payment_type', 'description')
        widgets = {
            'receiver': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible ', 'style': 'width: 100%;',
                       }),
            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: %; ', "onChange": 'ilceGetir()'}),

            'district': forms.Select(choices=CHOICES_WITH_BLANK,
                                     attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'id': 'ilce_id'}
                                     ),

            'exitDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'exitTime': forms.TextInput(attrs={'class': 'form-control timepicker'}),

            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Açıklama', 'rows': '2'}),

            'payment_type': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible', 'style': 'width: 100%;'}),

            'totalPrice': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ödenecek Tutar(₺)'})
        }
