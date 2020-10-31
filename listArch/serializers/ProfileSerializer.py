from rest_framework import serializers

from listArch.models import Company, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        depth = 3


class ProfileResponseSerializer(serializers.Serializer):
    data = ProfileSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
