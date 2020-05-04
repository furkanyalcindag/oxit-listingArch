from rest_framework import serializers

from kurye.models import District


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'
        depth = 3
