from rest_framework import serializers

from listArch.models import List


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'
        depth = 3
