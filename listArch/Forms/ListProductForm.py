from django import forms
from django.forms import ModelForm

from listArch.models import Product
from listArch.models.ListProduct import ListProduct
from listArch.models.Category import Category


class ListProductForm(ModelForm):
    class Meta:
        model = ListProduct
        fields = ('product',)
        widgets = {

        }

    product = forms.ModelMultipleChoiceField(queryset=Product.objects.all())

    # Overriding __init__ here allows us to provide initial
    # data for 'toppings' field
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)

        if kwargs.get('instance'):
            print(kwargs.get('instance').product.all())
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            forms.ModelForm.__init__(self, *args, **kwargs)
            initial['product'] = [t.pk for t in kwargs['instance'].category.all()]
            self.fields['product'].initial = initial['product']

        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['product'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                                'style': 'width: 100%;', 'data-select2-id': '7',
                                                'data-placeholder': 'Ürün Seçiniz'}
