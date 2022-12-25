from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer, IntegerField

from users.models import User, Location


class UserListSerializer(ModelSerializer):
    total_advertisements = IntegerField()
    location = StringRelatedField(many=True)

    class Meta:
        model = User
        exclude = ["password"]


class UserDetailViewSerializer(ModelSerializer):
    location = StringRelatedField(many=True)

    class Meta:
        model = User
        exclude = ["password"]


class LocationViewSetSerializer(ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"
