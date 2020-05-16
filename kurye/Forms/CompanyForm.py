from django import forms
from django.forms import ModelForm

from kurye.models.Company import Company


class CompanyForm(ModelForm):
    class Meta:
        model = Company

        fields = ('companyName', 'taxName', 'taxNumber')
        widgets = {
            'companyName': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Adı', 'rows': '2', 'required': 'required'}),
            'taxNumber': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Vergi Numarası', 'rows': '2', 'required': 'required'}),
            'taxName': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Vergi Dairesi', 'required': 'required'}),

        }
