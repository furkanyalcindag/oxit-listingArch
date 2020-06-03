from rest_framework import serializers

from kurye.models.TaskSituationTask import TaskSituationTask


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSituationTask
        fields = '__all__'
        depth = 4


class TaskResponseSerializer(serializers.Serializer):
    data = TaskSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
