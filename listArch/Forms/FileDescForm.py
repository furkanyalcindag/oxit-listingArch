from django import forms
from django.forms import ModelForm

from listArch.models.FileDesc import FileDesc


class FileDescForm(ModelForm):

    class Meta:
        model = FileDesc
        fields = ('file_title',)
        widgets = {
            'file_title': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Dosya Adı', 'required': 'required', 'value': '',
                       'name': 'download_file_name[eng]'}),



        }
