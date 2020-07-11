from django import forms
from django.forms import ModelForm

from listArch.models.OptionDesc import OptionDesc


class FeatureDescForm(ModelForm):
    class Meta:
        model = OptionDesc
        fields = ('description',)
        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Option Value Name', 'required': 'required'}),

        }
