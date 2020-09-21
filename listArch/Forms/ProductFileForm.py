from django import forms
from django.forms import ModelForm

from listArch.models.File import File
from listArch.models.ProductFile import ProductFile


class ProductFileForm(ModelForm):
    class Meta:
        model = ProductFile
        fields = ('product', 'file',)
        widgets = {}

    file = forms.ModelMultipleChoiceField(queryset=File.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            print(kwargs.get('instance').file.all())
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            forms.ModelForm.__init__(self, *args, **kwargs)
            initial['file'] = [t.pk for t in kwargs['instance'].file.all()]
            self.fields['file'].initial = initial['file']

        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['file'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%;', 'data-select2-id': '1', 'name': 'file',
                                            'data-placeholder': 'Dosya Seçiniz'}
