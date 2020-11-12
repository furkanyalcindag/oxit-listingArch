from django import forms
from django.forms import ModelForm

from listArch.models import Service
from listArch.models.Company import Company


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = (
            'name', 'address', 'phone', 'userDescription', 'logo', 'country', 'city', 'website', 'map', 'annualSales',
            'noOfEmployees', 'date', 'address_link', 'business_type', 'service',
        )

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Adı', 'required': 'required'}),
            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Adresi', 'required': 'required', 'rows': '4'}),
            'address_link': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Adresi Linki', 'required': 'required', 'rows': '4'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Telefonu', 'required': 'required'}),
            'userDescription': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '5', 'placeholder': 'Açıklama', 'required': 'required'}),
            'website': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Web Site Adresi', 'required': 'required'}),
            'map': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Konum Bilgisi', 'required': 'required'}),

            'country': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;'}),
            'city': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'type': 'date',
                       'autocomplete': 'off', 'format': '%d-%m-%Y',
                       }),
            'annualSales': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Yıllık Satış Tutarı'}),

            'noOfEmployees': forms.NumberInput(
                attrs={'class': 'form-control ', 'placeholder': 'Çalışan Sayısı'}),
            'business_type': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible', 'name': 'type',
                       'style': 'width: 100%;', 'required': 'required'}),

        }

    service = forms.ModelMultipleChoiceField(queryset=Service.objects.all())

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            print(kwargs.get('instance').service.all())
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            forms.ModelForm.__init__(self, *args, **kwargs)
            initial['service'] = [t.pk for t in kwargs['instance'].service.all()]
            self.fields['service'].initial = initial['service']

        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['service'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                               'style': 'width: 100%;', 'data-select2-id': '1',
                                               'required': 'false', }
