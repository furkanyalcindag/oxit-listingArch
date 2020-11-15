from django import forms
from django.forms import ModelForm
from listArch.models.ProductImage import ProductImage


class ProductImageForm(ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = ProductImage
        fields = ('image',)
        widgets = {

        }
