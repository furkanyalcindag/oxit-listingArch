from django import forms
from django.forms import ModelForm

from listArch.models.Customer import Customer


class CustomerForm(ModelForm):
    isCompany = forms.BooleanField(required=False)

    class Meta:
        model = Customer
        fields = ('isCompany',)
        widgets = {
        }
