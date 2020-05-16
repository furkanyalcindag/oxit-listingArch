from django import forms
from django.forms import ModelForm

from kurye.models.Profile import Profile


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile

        fields = (
            'profileImage', 'address', 'mobilePhone', 'phone')
        widgets = {
            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'placeholder': 'Adres', 'rows': '4'}),
            'mobilePhone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': '(0xxx) xxx xxxx', 'required': 'required'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': '(0xxx) xx xx',
                       'maxlength': '10', 'minlength': '10'}),

        }
