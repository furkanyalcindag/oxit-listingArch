from rest_framework import serializers

from listArch.models import OptionValue, OptionValueDesc


class OptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionValue
        fields = '__all__'
        depth = 3
