from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from advertisements.models import Category, Advertisement


class CategoryViewSetSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class AdvertisementListSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Advertisement
        fields = ["id", "name", "author", "price"]
