from django import forms
from django.forms import ModelForm

from listArch.models import BusinessType


class BusinessTypeForm(ModelForm):
    isProduct_based = forms.BooleanField(required=False)

    class Meta:
        model = BusinessType
        fields = ('key', 'isProduct_based', )
        widgets = {
            'key': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Profil Adı', 'required': 'required',
                       'name': 'key'}),

        }
