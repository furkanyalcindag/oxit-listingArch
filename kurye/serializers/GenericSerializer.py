from rest_framework import serializers

from kurye.models import Log


class GenericModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = []
        depth = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Meta.model = kwargs['context']['request']['model']
        self.Meta.fields = kwargs['context']['request']['fields']


class DataTableSerializer(serializers.Serializer):
    data = serializers.SerializerMethodField('get_child_serializer')
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()

    serializers.SerializerMethodField('get_child_serializer')

    def get_child_serializer(self, obj):
        serializer_context = {'request': self.context, "obj": obj}
        logs = Log.objects.all()
        serializer = GenericModelSerializer(many=True, context=serializer_context)
        return serializer.data
