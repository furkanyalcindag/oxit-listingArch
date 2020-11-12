from django.forms import ModelForm

from listArch.models import Video

class VideoForm(ModelForm):

    class Meta:
        model = Video
        fields = ('file',)
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False