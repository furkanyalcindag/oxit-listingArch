from django import forms
from django.forms import ModelForm

from listArch.models.File import File

CHOICES_WITH_BLANK = (
    ('', '--------'),
    ('F2', 'F2'),
    ('F3', 'F3'),
    ('C2', 'C2'),
    ('C3', 'C3'),
    ('CAD FILE', 'CAD FILE'),
    ('BIM FILE', 'BIM FILE'),
    ('PDF GENERAL CATAGLOUGE', 'PDF GENERAL CATAGLOUGE'),
    ('ETHICS', 'ETHICS'),
    ('TECHNICAL FILES', 'TECHNICAL FILES'),
    ('WARRANTY', 'WARRANTY'),
    ('LEGAL NOTES', 'LEGAL NOTES'),
    ('GENERAL SALE NOTES', 'GENERAL SALE NOTES'),
    ('COMPANY PROFILE', 'COMPANY PROFILE'),
    ('COMPANY REPORTS', 'COMPANY REPORTS'),

)


class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ('file', 'file_title', 'file_type', 'category', 'company')
        widgets = {
            'file_type': forms.Select(choices=CHOICES_WITH_BLANK,
                                      attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%;', 'required': 'required'}),
            'file': forms.FileInput(attrs={'required': 'required'}),
            'category': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%;', 'onchange': 'get_files()',
                                            'required': 'required'}),
            'company': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;', 'onchange': 'get_files()', 'required': 'required'}),
            'file_title': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Dosya Adı', 'required': 'required', 'value': '',
                       'name': 'download_file_name[TR]', }),

        }
