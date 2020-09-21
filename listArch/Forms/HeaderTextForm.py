from django import forms
from django.forms import ModelForm

from listArch.models import HeaderText


class HeaderTextForm(ModelForm):
    isActive = forms.BooleanField(required=False)

    class Meta:
        model = HeaderText
        fields = ('isActive',)
