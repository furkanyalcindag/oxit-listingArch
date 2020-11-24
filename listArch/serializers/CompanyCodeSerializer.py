from rest_framework import serializers

from listArch.models import Company, CompanyCode


class CompanyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyCode
        fields = '__all__'
        depth = 3



