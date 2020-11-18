from django import forms
from django.forms import ModelForm

from listArch.models.Option import Option


class OptionForm(ModelForm):
    isBasic = forms.BooleanField(widget=forms.CheckboxInput(),required=False)

    class Meta:
        model = Option
        fields = ('isBasic',)
        widgets = {

        }
