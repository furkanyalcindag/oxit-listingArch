from django.forms import ModelForm

from listArch.models import BlogImage


class BlogDescImageForm(ModelForm):
    class Meta:
        model = BlogImage
        fields = ('image',)
        widgets = {

        }
