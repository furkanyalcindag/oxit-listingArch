from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from kurye.models.Settings import Settings


class SettingCourierPrimForm(ModelForm):
    class Meta:
        model = Settings
        fields = ('name', 'value')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required','readonly': 'readonly',
                       }),
            'value': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required',
                       }),

        }
