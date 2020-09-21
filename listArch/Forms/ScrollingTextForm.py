from django import forms
from django.forms import ModelForm

from listArch.models import ScrollingText


class ScrollingTextForm(ModelForm):
    isActive = forms.BooleanField(required=False)

    class Meta:
        model = ScrollingText
        fields = ('isActive',)
