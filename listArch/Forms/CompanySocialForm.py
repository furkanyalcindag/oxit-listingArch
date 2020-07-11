from django import forms
from django.forms import ModelForm

from listArch.models.CompanySocialAccount import CompanySocialAccount


class CompanySocialForm(ModelForm):

    class Meta:
        model = CompanySocialAccount
        fields = ('social_account', )
        widgets = {
            'social_account': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Hesap Linki', 'required': 'required'}),



        }

