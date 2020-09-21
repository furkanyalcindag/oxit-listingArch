from rest_framework import serializers

from listArch.models.OptionValueDesc import OptionValueDesc


class OptionValueDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionValueDesc
        fields = '__all__'
        depth = 3
