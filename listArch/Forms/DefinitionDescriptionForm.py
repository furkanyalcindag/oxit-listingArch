from django import forms
from django.forms import ModelForm

from listArch.models.DefinitionDescription import DefinitionDescription


class DefinitionDescriptionForm(ModelForm):
    class Meta:
        model = DefinitionDescription
        fields = ('description', 'title_desc',)
        widgets = {
            'description': forms.Textarea(
                attrs={'class': 'form-control textarea', 'id': 'content', 'name': 'content', 'placeholder': 'Definition',
                       'required': 'required', 'rows': 5}),
            'title_desc': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Definition Title', 'required': 'required'}),

        }
