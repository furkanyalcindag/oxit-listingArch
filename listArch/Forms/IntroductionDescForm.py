from django import forms
from django.forms import ModelForm

from listArch.models import IntroductionPageDesc


class IntroductionDescForm(ModelForm):
    class Meta:
        model = IntroductionPageDesc
        fields = ('description',)
        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),

        }
