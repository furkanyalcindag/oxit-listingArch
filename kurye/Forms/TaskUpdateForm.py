from django import forms
from django.forms import ModelForm

from kurye.models.Task import Task


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task

        fields = ('description',)

        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Açıklama'}),
        }
