from django import forms
from django.forms import ModelForm

from listArch.models.Product import Product
from listArch.models.Category import Category


class ProductForm(ModelForm):
    isActive = forms.BooleanField(required=False)
    isAdvert = forms.BooleanField(required=False)

    class Meta:
        model = Product
        fields = (
            'category', 'isActive', 'company_code', 'code', 'cover_image', 'isAdvert', 'price',
            'related_product', 'file', 'code2',)
        widgets = {
            'company_code': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Firma Ürün Kodu', 'required': 'required'}),
            'code': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Ürün Kodu', 'required': 'required'}),
            'code2': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Ürün Kodu2', 'required': 'required'}),
            'price': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Fiyat($)','required': 'required'}),
            'cover_image': forms.FileInput(
                attrs={'class': 'form-control', 'required': 'required'}),
        }

    categories = Category.objects.filter(isActive=True)
    category = forms.ModelMultipleChoiceField(queryset=categories, required=True)
    related_product = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), required=False)

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
            initial['related_product'] = [t.pk for t in kwargs['instance'].related_product.all()]

            self.fields['category'].initial = initial['category']
            self.fields['related_product'].initial = initial['related_product']

        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['category'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                                'style': 'width: 100%;', 'data-select2-id': '7',
                                                'data-placeholder': 'Kategori Seçiniz'}
        self.fields['related_product'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                                       'style': 'width: 100%;', 'data-select2-id': '1',
                                                       'data-placeholder': 'Benzer Ürün Seçiniz'}
