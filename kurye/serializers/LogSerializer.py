from rest_framework import serializers

from kurye.models import Log


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['content', 'creationDate']
        depth = 4


class LogResponseSerializer(serializers.Serializer):
    data = LogSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
