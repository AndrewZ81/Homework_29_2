from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, IntegerField

from users.models import User, Location


class UserListSerializer(ModelSerializer):
    total_advertisements = IntegerField()
    location = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"


class LocationViewSetSerializer(ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"
