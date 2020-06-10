from django import forms
from django.forms import ModelForm

from kurye.models.Request import Request

CHOICES_WITH_BLANK = (
    ('', '-------'),

)


class RequestForm(ModelForm):
    class Meta:
        model = Request

        fields = (
            'exitTime', 'exitDate', 'totalPrice',
            'payment_type', 'description', 'city', 'district')
        widgets = {

            'exitDate': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'value': ''}),

            'exitTime': forms.TextInput(attrs={'class': 'form-control timepicker', 'required': 'required'}),

            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Açıklama', 'rows': '2'}),

            'payment_type': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible', 'style': 'width: 100%;',
                       'required': 'required'}),

            'totalPrice': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Ödenecek Tutar(₺)', 'required': 'required'}),
            'city': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%; ', "onChange": 'ilceGetir()', 'required': 'required'}),
            'neighborhood': forms.Select(
                attrs={'class': 'form-control', 'placeholder': 'Mahalle', 'rows': '2', 'required': 'required', }),

            'district': forms.Select(choices=CHOICES_WITH_BLANK,
                                     attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'id': 'ilce_id', 'required': 'required'}
                                     )
        }
