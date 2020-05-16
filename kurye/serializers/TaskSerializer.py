from rest_framework import serializers

from kurye.models.TaskSituationTask import TaskSituationTask


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSituationTask
        fields = '__all__'
        depth = 4
