from django import forms
from django.forms import ModelForm

from listArch.models.Category import Category


class CategoryForm(ModelForm):
    is_parent = forms.BooleanField(required=False)

    class Meta:
        model = Category
        fields = ('name', 'is_parent', 'url', )
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Kategori Adı', 'required': 'required'}),

            'url': forms.TextInput(
                attrs={'class': 'form-control ', 'name': 'url', 'id': 'url'}),

        }



