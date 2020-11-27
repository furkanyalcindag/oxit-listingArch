from rest_framework import serializers

from listArch.models import FileDesc


class FileDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileDesc
        fields = '__all__'
        depth = 3
