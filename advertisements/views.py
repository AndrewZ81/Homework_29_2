import collections
import json
from typing import List, Dict

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Category, Advertisement
from advertisements.serializers import CategoryViewSetSerializer, AdvertisementListViewSerializer, \
    AdvertisementDetailViewSerializer
from users.models import User


def show_main_page(request) -> JsonResponse:
    return JsonResponse({"status": "ok"}, status=200)


class CategoryViewSet(ModelViewSet):
    """
    Кратко отображает таблицу Категории (сортирует записи по алфавиту),
    детально отображает запись (выбранную по id),
    создаёт новую запись,
    редактирует запись (выбранную по id),
    удаляет запись (выбранную по id)
    """

    queryset = Category.objects.all().order_by("name")
    serializer_class = CategoryViewSetSerializer


class AdvertisementListView(ListAPIView):
    """
    Отображает таблицу Advertisement, при запросе
    фильтрует записи по категориям
    """
    queryset = Advertisement.objects.all().order_by("-price")
    serializer_class = AdvertisementListViewSerializer

    def list(self, request, *args, **kwargs):

        categories = request.GET.getlist("cat")
        if categories:
            self.queryset = self.queryset.filter(category__in=categories)

        text = request.GET.get("text")
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location")
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get("price_from")
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get("price_to")
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(self, request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class AdvertisementCreateView(CreateView):
    """
    Cоздаёт новую запись Advertisement
    """
    model = Advertisement
    fields = "__all__"

    def post(self, request, *args, **kwargs) -> JsonResponse:
        advertisement_data: Dict[str, int | str] = json.loads(request.body)

        author = get_object_or_404(User, username=advertisement_data["author"])
        category = get_object_or_404(Category, id=advertisement_data["category_id"])

        advertisement: Advertisement = Advertisement.objects.create(
            name=advertisement_data.get("name"),
            author=author,
            price=advertisement_data.get("price"),
            description=advertisement_data.get("description"),
            image=advertisement_data.get("image"),
            is_published=advertisement_data.get("is_published"),
            category=category
        )

        response_as_dict: Dict[str, int | str] = {
            "id": advertisement.id,
            "name": advertisement.name,
            "author": author.username,
            "price": advertisement.price,
            "description": advertisement.description,
            "address": [
                _location.name for _location in advertisement.author.location.all()
            ],
            "image": advertisement.image.url if advertisement.image else None,
            "is_published": advertisement.is_published,
            "category": category.name
        }
        return JsonResponse(response_as_dict, json_dumps_params={"ensure_ascii": False, "indent": 4})


class AdvertisementDetailView(RetrieveAPIView):
    """
    Делает выборку записи из таблицы Объявления по id
    """
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementDetailViewSerializer


@method_decorator(csrf_exempt, name="dispatch")
class AdvertisementUpdateView(UpdateView):
    """
    Редактирует запись Advertisement
    """
    model = Advertisement
    fields = "__all__"

    def patch(self, request, *args, **kwargs) -> JsonResponse:
        super().post(request, *args, **kwargs)
        advertisement_data: Dict[str, str | int] = json.loads(request.body)

        if "name" in advertisement_data:
            self.object.name = advertisement_data["name"]
        if "price" in advertisement_data:
            self.object.price = advertisement_data["price"]
        if "description" in advertisement_data:
            self.object.description = advertisement_data["description"]

        self.object.save()

        response_as_dict: Dict[str, int | str] = {
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "address": [
                _location.name for _location in self.object.author.location.all()
            ],
            "image": self.object.image.url if self.object.image else None,
            "is_published": self.object.is_published,
            "category_id": self.object.category.id,
            "category_name": self.object.category.name
        }
        return JsonResponse(response_as_dict, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name="dispatch")
class AdvertisementDeleteView(DeleteView):
    """
    Удаляет запись Advertisement
    """
    model = Advertisement
    success_url = "/"

    def delete(self, request, *args, **kwargs) -> JsonResponse:
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdvertisementUploadImage(UpdateView):
    """
    Добавляет изображение к записи Advertisement по id
    """
    model = Advertisement
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        self.object: Advertisement = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()

        response_as_dict: Dict[str, int | str] = {
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "address": [
                _location.name for _location in self.object.author.location.all()
            ],
            "image": self.object.image.url,
            "is_published": self.object.is_published,
            "category_id": self.object.category.id,
            "category_name": self.object.category.name
        }
        return JsonResponse(response_as_dict, json_dumps_params={"ensure_ascii": False, "indent": 4})
