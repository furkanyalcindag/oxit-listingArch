from django import forms
from django.forms import ModelForm

from listArch.models.OptionValue import OptionValue


class FeatureValueForm(ModelForm):
    class Meta:
        model = OptionValue
        fields = ('value',)
        widgets = {
            'value': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Özellik Değeri', 'required': 'required'}),

        }
