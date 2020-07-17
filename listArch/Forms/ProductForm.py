from django import forms
from django.forms import ModelForm

from listArch.models import Product
from listArch.models.Option import Option


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('company')

