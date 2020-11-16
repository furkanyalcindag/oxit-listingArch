from django import forms
from django.forms import ModelForm

from listArch.models import IntroductionPage, Product


class IntroductionForm(ModelForm):
    isActive = forms.BooleanField(required=False)

    class Meta:
        model = IntroductionPage
        fields = ('key', 'category', 'isActive', 'title', 'product')
        widgets = {
            'key': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'category': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible', 'name': 'type',
                       'style': 'width: 100%;', 'required': 'required'}),
            'title': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%;', 'required': 'required'}),

        }

    product = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), required=False)

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
            initial['product'] = [t.pk for t in kwargs['instance'].product.all()]
            self.fields['product'].initial = initial['product']

        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['product'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                               'style': 'width: 100%;', 'data-select2-id': '7',
                                               'data-placeholder': ' Ürünleri Seçiniz'}
