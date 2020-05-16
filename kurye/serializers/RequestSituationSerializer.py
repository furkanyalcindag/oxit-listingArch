from rest_framework import serializers

from kurye.models import Request
from kurye.models.RequestSituationRequest import RequestSituationRequest


class RequestSituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestSituationRequest
        fields = '__all__'
        depth = 4
