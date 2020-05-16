from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Adınız', 'value': '', 'required': 'required',
                      }),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Soyadınız', 'required': 'required',
                       }),

            'email': forms.EmailInput(
                attrs={'class': 'form-control ', 'placeholder': ' Soyadınız', 'required': 'required',
                       }),

        }
