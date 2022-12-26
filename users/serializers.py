from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users.models import User, Location


class UserListViewSerializer(ModelSerializer):
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


class UserCreateViewSerializer(ModelSerializer):
    location = SlugRelatedField(
        required=False,
        many=True,
        slug_field="name",
        queryset=Location.objects.all()
    )

    def is_valid(self, *, raise_exception=False):
        user_locations = self.initial_data.pop("location", [])
        setattr(self, "_location", user_locations)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        new_user = User.objects.create(**validated_data)
        for loc in self._location:
            new_location, _ = Location.objects.get_or_create(name=loc)
            new_user.location.add(new_location)
        return new_user

    class Meta:
        model = User
        fields = "__all__"


class UserUpdateViewSerializer(ModelSerializer):
    location = SlugRelatedField(
        required=False,
        many=True,
        slug_field="name",
        queryset=Location.objects.all()
    )

    def is_valid(self, *, raise_exception=False):
        user_locations = self.initial_data.pop("location", [])
        setattr(self, "_location", user_locations)
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        for loc in self._location:
            new_location, _ = Location.objects.get_or_create(name=loc)
            user.location.add(new_location)
        return user

    class Meta:
        model = User
        fields = "__all__"


class LocationViewSetSerializer(ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"
