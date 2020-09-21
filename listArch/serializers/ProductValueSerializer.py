from rest_framework import serializers

from listArch.models import ProductOptionValue


class ProductValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionValue
        fields = '__all__'
        depth = 3
