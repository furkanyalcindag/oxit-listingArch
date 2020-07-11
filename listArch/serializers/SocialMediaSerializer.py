from rest_framework import serializers

from listArch.models.SocialMedia import SocialMedia


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'
        depth = 3
