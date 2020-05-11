from django import forms
from django.forms import ModelForm

from kurye.models import TaskSituations
from kurye.models.Task import Task


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task

        fields = ('courier', 'task_situation')

    task_situation = forms.ModelChoiceField(queryset=TaskSituations.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control select2 select2-hidden-accessible', 'style': 'width: 100%;'}))
