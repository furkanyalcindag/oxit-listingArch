from django import forms
from django.forms import ModelForm

from listArch.models.Option import Option


class FeatureForm(ModelForm):
    class Meta:
        model = Option
        fields = ('key', 'type',)
        widgets = {
            'key': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Özellik Adı', 'required': 'required'}),
            'type': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible', 'name': 'type', 'id': 'input-type',
                       'style': 'width: 100%;', 'required': 'required'}),

        }
