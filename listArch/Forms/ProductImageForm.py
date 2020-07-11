from django import forms
from django.forms import ModelForm
from listArch.models.ProductImage import ProductImage


class ProductImageForm(ModelForm):
    is_parent = forms.BooleanField(required=False)

    class Meta:
        model = ProductImage
        fields = ('image',)
        widgets = {

        }



