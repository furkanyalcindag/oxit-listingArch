from django.forms import ModelForm
from listArch.models.ProductImage import ProductImage


class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image',)
        widgets = {

        }
