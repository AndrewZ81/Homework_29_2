from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer

from advertisements.models import Category, Advertisement
from users.models import User, Location


class CategoryViewSetSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class AdvertisementListViewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    category = StringRelatedField()
    locations = SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ["id", "name", "author", "price", "category", "locations"]

    def get_locations(self, ad):
        setattr(ad, "locations", [location.name for location in ad.author.location.all()])
        return ad.locations


class AdvertisementDetailViewSerializer(ModelSerializer):
    author_id = PrimaryKeyRelatedField(queryset=User.objects.all())
    author = SlugRelatedField(
        read_only=True,
        slug_field="username",
    )
    category_id = PrimaryKeyRelatedField(queryset=Category.objects.all())
    category = StringRelatedField()
    locations = SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = "__all__"

    def get_locations(self, ad):
        setattr(ad, "locations", [location.name for location in ad.author.location.all()])
        return ad.locations
