from rest_framework import serializers

from listArch.models import  OptionValue


class OptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionValue
        fields = '__all__'
        depth = 3
