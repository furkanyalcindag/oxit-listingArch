from django import forms
from django.forms import ModelForm

from listArch.models.Product import Product
from listArch.models.Category import Category


class ProductForm(ModelForm):
    isActive = forms.BooleanField(required=False)
    isSponsor = forms.BooleanField(required=False)
    isAdvert = forms.BooleanField(required=False)

    class Meta:
        model = Product
        fields = (
            'category', 'isActive', 'company_code', 'code', 'isSponsor', 'cover_image', 'isAdvert', 'price')
        widgets = {
            'company_code': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Ürün Kodu'}),
            'code': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Ürün Kodu'}),
            'price': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Fiyat(₺)', 'required': 'required'}),
        }

    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    # Overriding __init__ here allows us to provide initial
    # data for 'toppings' field
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)

        if kwargs.get('instance'):
            print(kwargs.get('instance').category.all())
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            forms.ModelForm.__init__(self, *args, **kwargs)
            initial['category'] = [t.pk for t in kwargs['instance'].category.all()]
            self.fields['category'].initial = initial['category']

        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['category'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                                'style': 'width: 100%;', 'data-select2-id': '7',
                                                'data-placeholder': 'Kategori Seçiniz'}
