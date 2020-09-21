from django import forms
from django.forms import ModelForm

from listArch.models.ProductDefinition import ProductDefinition


class ProductDefinitionForm(ModelForm):
    class Meta:
        model = ProductDefinition
        fields = ('product', 'definition',)
        widgets = {


        }
