from django import forms
from django.forms import ModelForm

from listArch.models import GraphicValue


class GraphicValueForm(ModelForm):
    class Meta:
        model = GraphicValue
        fields = ('min', 'max', 'current_value',  'middle','unit')
        widgets = {

            'min': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Minimum Değer', 'required': 'required'}),
            'max': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Maksimum Değer', 'required': 'required'}),
            'current_value': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Maksimum Değer', 'required': 'required'}),
            'unit': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Birim', 'required': 'required'}),
            'middle': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Ara Değer', 'required': 'required'}),

        }
