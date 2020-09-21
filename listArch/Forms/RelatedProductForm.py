from django import forms
from django.forms import ModelForm
from listArch.models import RelatedProduct, Product


class RelatedProductForm(ModelForm):
    class Meta:
        model = RelatedProduct
        fields = ('related_product',)
        widgets = {

        }

    related_product = forms.ModelMultipleChoiceField(queryset=Product.objects.all())

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            print(kwargs.get('instance').related_product.all())
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            forms.ModelForm.__init__(self, *args, **kwargs)
            initial['related_product'] = [t.pk for t in kwargs['instance'].related_product.all()]
            self.fields['related_product'].initial = initial['related_product']

        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['related_product'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                               'style': 'width: 100%;', 'data-select2-id': '1', 'required': 'false',
                                               'data-placeholder': 'Ürün Seçiniz'}
