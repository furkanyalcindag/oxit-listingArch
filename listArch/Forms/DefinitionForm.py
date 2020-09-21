from django import forms
from django.forms import ModelForm

from listArch.models.Definition import Definition


class DefinitionForm(ModelForm):
    class Meta:
        model = Definition
        fields = ('key',)
        widgets = {
            'key': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),

        }
