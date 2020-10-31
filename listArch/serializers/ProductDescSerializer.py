from rest_framework import serializers

from listArch.models import ProductDesc


class ProductDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDesc
        fields = '__all__'
        depth = 3
