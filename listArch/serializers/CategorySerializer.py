from rest_framework import serializers

from listArch.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth = 3


class CategoryResponseSerializer(serializers.Serializer):
    data = CategorySerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
