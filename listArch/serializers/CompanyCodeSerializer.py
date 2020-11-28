from rest_framework import serializers

from listArch.models.CompanyCode import  CompanyCode


class CompanyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyCode
        fields = '__all__'
        depth = 3



