from django import forms
from django.forms import ModelForm

from listArch.models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('website', 'address', 'country', 'city', 'profile_name', 'image', 'map', 'phone')
        widgets = {

            'website': forms.TextInput(
                attrs={'class': 'form-control '}),
            'map': forms.TextInput(
                attrs={'class': 'form-control '}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': '+905305426989'}),
            'address': forms.Textarea(
                attrs={'class': 'form-control '}),
            'country': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;'}),
            'city': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;'}),
            'profile_name': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;', 'required': 'required'}),

        }
