from django import forms
from django.forms import ModelForm

from listArch.models.ProductCategory import ProductCategory
from listArch.models.Category import Category


class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('category',)

    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

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
            self.fields['category'].initial = {'multi_field':
                                                   [category for category in
                                                    Category.objects.all().values_list('id', flat=True)]}

        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['category'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                                'style': 'width: 100%;',
                                                'data-placeholder': 'Kategori Seçin'}
