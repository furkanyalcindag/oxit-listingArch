from django import forms
from django.forms import ModelForm

from listArch.models.Company import Company


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = (
            'name', 'address', 'phone', 'userDescription', 'logo', 'country', 'city', 'website', 'map', 'annualSales',
            'noOfEmployees', 'date', 'address_link',
        )

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Adı', 'required': 'required'}),
            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Adresi', 'required': 'required', 'rows': '4'}),
            'address_link': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Adresi Linki', 'required': 'required', 'rows': '4'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Telefonu', 'required': 'required'}),
            'userDescription': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '5', 'placeholder': 'Açıklama', 'required': 'required'}),
            'website': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Web Site Adresi', 'required': 'required'}),
            'map': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Konum Bilgisi', 'required': 'required'}),

            'country': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;'}),
            'city': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'type': 'date',
                       'autocomplete': 'off', 'format': '%d-%m-%Y',
                       }),
            'annualSales': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Yıllık Satış Tutarı'}),

            'noOfEmployees': forms.NumberInput(
                attrs={'class': 'form-control ', 'placeholder': 'Çalışan Sayısı'}),

        }
