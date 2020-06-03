from rest_framework import serializers

from kurye.models import Neighborhood


class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = ['id', 'city', 'district', 'neighborhood_name', 'price']
        depth = 3


class NeighborhoodResponseSerializer(serializers.Serializer):
    data = NeighborhoodSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
