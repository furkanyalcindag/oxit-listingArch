from django import forms
from django.forms import ModelForm

from listArch.models import Option


class OptionForm(ModelForm):
    isAdvert = forms.BooleanField(required=False)

    class Meta:
        model = Option
        fields = ('isBasic',)
        widgets = {

        }
