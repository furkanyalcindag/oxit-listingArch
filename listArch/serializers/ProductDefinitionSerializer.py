from rest_framework import serializers

from listArch.models.DefinitionDescription import DefinitionDescription


class ProductDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefinitionDescription
        fields = '__all__'
        depth = 3
