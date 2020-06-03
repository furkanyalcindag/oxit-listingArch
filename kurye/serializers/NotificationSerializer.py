from rest_framework import serializers

from kurye.models.Company import Company
from kurye.models.Notification import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'key', 'message', 'creationDate', 'isRead']
        depth = 4


class NotificationResponseSerializer(serializers.Serializer):
    data = NotificationSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
