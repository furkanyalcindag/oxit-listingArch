from django import forms
from django.forms import ModelForm

from listArch.models.Customer import Customer


class CustomerUpdateForm(ModelForm):
    isCompany = forms.BooleanField(required=False)

    class Meta:
        model = Customer
        fields = ('isCompany', 'companyMail', 'companyName', 'companyAddress', 'companyPhone')
        widgets = {

            'companyName': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'companyPhone': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'companyAddress': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'companyMail': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
        }
