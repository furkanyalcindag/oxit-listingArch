from django import forms
from django.forms import ModelForm

from listArch.models import CategoryDesc


class CategoryDescForm(ModelForm):
    class Meta:
        model = CategoryDesc
        fields = ('description', 'definition', 'page_description')
        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Kategori Adı', 'required': 'required'}),
            'definition': forms.Textarea(
                attrs={'class': 'form-control textarea', 'id': 'content', 'name': 'content',
                       'placeholder': 'İçerik ...',
                       'required': 'required', 'rows': 10, }),
            'page_description': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Sayfa Yazısı', }),

        }
