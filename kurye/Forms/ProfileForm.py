from django import forms
from django.forms import ModelForm

from kurye.models.Profile import Profile

CHOICES_WITH_BLANK = (
    ('', '--------'),

)


class ProfileForm(ModelForm):

    class Meta:
        model = Profile

        fields = (
            'profileImage', 'address', 'mobilePhone', 'tc', 'city',
            'district', 'phone')
        widgets = {
            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'placeholder': 'Adres', 'rows': '4'}),
            'mobilePhone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': '(0xxx) xxx xxxx', 'required': 'required'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': '(0xxx) xx xx',
                       'maxlength': '10', 'minlength': '10'}),

            'tc': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'T.C. Kimlik Numarası',
                       'maxlength': '11', 'minlength': '11'}),


            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', "onChange": 'ilceGetir()'}),

            'district': forms.Select(choices=CHOICES_WITH_BLANK,
                                     attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'id': 'ilce_id'}
                                     )

        }
