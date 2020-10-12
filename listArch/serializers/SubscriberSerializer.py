from rest_framework import serializers
from listArch.models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'
        depth = 3


class SubscriberResponseSerializer(serializers.Serializer):
    data = SubscriberSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
