from django import forms
from django.forms import ModelForm

from listArch.models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('website', 'address', 'country', 'city', 'profile_name', 'image', 'map')
        widgets = {

            'website': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'map': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'country': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;'}),
            'city': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;'}),
            'profile_name': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;'}),

        }
