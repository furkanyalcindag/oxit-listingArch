from django import forms
from django.forms import ModelForm

from listArch.models import IntroductionPage


class IntroductionForm(ModelForm):
    isActive = forms.BooleanField(required=False)

    class Meta:
        model = IntroductionPage
        fields = ('key', 'category', 'isActive', 'title')
        widgets = {
            'key': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'category': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible', 'name': 'type',
                       'style': 'width: 100%;', 'required': 'required'}),
            'title': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;', 'required': 'required'}),

        }
