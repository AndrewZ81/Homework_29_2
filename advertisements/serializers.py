from rest_framework.serializers import Serializer, CharField, IntegerField


class CategorySerializer(Serializer):
    id = IntegerField()
    name = CharField(max_length=200)
