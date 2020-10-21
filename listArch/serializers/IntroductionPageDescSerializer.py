from rest_framework import serializers

from listArch.models import IntroductionPageDesc


class IntroductionPageDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntroductionPageDesc
        fields = '__all__'
        depth = 3
