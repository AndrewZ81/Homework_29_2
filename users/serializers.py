from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users.models import User, Location


class UserListSerializer(ModelSerializer):
    total_advertisements = SerializerMethodField()
    location = StringRelatedField(many=True)

    class Meta:
        model = User
        exclude = ["password"]

    def get_total_advertisements(self, user):
        return user.advertisement_set.filter(is_published=True).count()


class UserDetailViewSerializer(ModelSerializer):
    location = StringRelatedField(many=True)

    class Meta:
        model = User
        exclude = ["password"]


class LocationViewSetSerializer(ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"
