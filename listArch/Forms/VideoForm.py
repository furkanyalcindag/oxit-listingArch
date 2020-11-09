from django.forms import ModelForm

from listArch.models import Video

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ('file',)
        widgets = {

        }