from django import forms
from django.forms import ModelForm

from listArch.models.Contact import Contact


class ContactForm(ModelForm):
    isActive = forms.BooleanField(required=False)

    class Meta:
        model = Contact
        fields = ('email', 'phone', 'isActive')
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email',
                       'required': 'required', }),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Telefon'})
        }
