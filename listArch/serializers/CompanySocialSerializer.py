from rest_framework import serializers

from listArch.models.CompanySocialAccount import CompanySocialAccount


class CompanySocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySocialAccount
        fields = '__all__'
        depth = 3
