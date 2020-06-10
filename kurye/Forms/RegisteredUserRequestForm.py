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
            'payment_type', 'description', 'neighborhood')
        widgets = {
            'receiver': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible ', 'style': 'width: 100%;',
                       'required': 'required'}),
            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'required': 'required', 'style': 'width: %; ', "onChange": 'ilceGetir()'}),

            'district': forms.Select(choices=CHOICES_WITH_BLANK,
                                     attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'required': 'required', 'style': 'width: 100%; ', 'id': 'ilce_id'}
                                     ),
            'neighborhood': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Mahalle', 'rows': '2', 'required': 'required'}),

            'exitDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'exitTime': forms.TextInput(attrs={'class': 'form-control timepicker', 'required': 'required'}),

            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Açıklama', 'rows': '2'}),

            'payment_type': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible', 'style': 'width: 100%;',
                       'required': 'required'}),

            'totalPrice': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Ödenecek Tutar(₺)', 'required': 'required'})
        }
