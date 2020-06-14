from django import forms
from django.forms import ModelForm

from kurye.models.Courier import Courier

CHOICES_WITH_BLANK = (
    ('', '-------'),

)


class CourierForm(ModelForm):
    class Meta:
        model = Courier

        fields = ('type',)
        widgets = {

            'type': forms.Select(choices=CHOICES_WITH_BLANK,
                                 attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', 'required': 'required'}),

        }
