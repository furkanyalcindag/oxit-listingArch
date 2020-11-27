from rest_framework import serializers

from listArch.models import FileDesc, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        depth = 3
