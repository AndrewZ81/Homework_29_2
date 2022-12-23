from rest_framework.serializers import ModelSerializer

from advertisements.models import Category, Advertisement


class CategoryListSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class AdvertisementListSerializer(ModelSerializer):

    class Meta:
        model = Advertisement
        fields = ["id", "name", "author_id", "price"]
