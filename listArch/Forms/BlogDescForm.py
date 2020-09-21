from django import forms
from django.forms import ModelForm

from listArch.models.BlogDesc import BlogDesc


class BlogDescForm(ModelForm):
    class Meta:
        model = BlogDesc
        fields = ('description', 'title_desc')
        widgets = {
            'description': forms.Textarea(
                attrs={'class': 'form-control textarea', 'id': 'content', 'name': 'content', 'placeholder': 'İçerik ...',
                       'required': 'required', 'rows': 10, }),
            'title_desc': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Başlık ...', 'required': 'required'})
        }
