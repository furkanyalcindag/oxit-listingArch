from django import forms
from django.forms import ModelForm

from kurye.models import Request


class RequestForm(ModelForm):
    class Meta:
        model = Request

        fields = (
            'exitTime', 'exitDate', 'totalPrice',
            'payment_type', 'description')
        widgets = {

            'exitDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'exitTime': forms.TextInput(attrs={'class': 'form-control timepicker'}),

            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Açıklama', 'rows': '2'}),



            'payment_type': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible', 'style': 'width: 100%;'}),

            'totalPrice': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ödenecek Tutar(₺)'})
        }
