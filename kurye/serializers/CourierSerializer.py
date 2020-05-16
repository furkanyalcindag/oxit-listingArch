from rest_framework import serializers

from kurye.models.Courier import Courier


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'
        depth = 4
