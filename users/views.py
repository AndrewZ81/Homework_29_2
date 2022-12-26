import collections
import json
from typing import List, Dict

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User, Location
from users.serializers import UserListSerializer, LocationViewSetSerializer, UserDetailViewSerializer


class UserListView(ListAPIView):
    """
    Кратко отображает таблицу Пользователи
    """
    queryset = User.objects.all().order_by("username")
    serializer_class = UserListSerializer


class UserDetailView(RetrieveAPIView):
    """
    Делает выборку записи из таблицы Пользователи по id
    """
    queryset = User.objects.all()
    serializer_class = UserDetailViewSerializer


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    """
    Cоздаёт новую запись User
    """
    model = User
    fields = "__all__"

    def post(self, request, *args, **kwargs) -> JsonResponse:
        user_data: Dict[str, int | str] = json.loads(request.body)

        user: User = User.objects.create(
            username=user_data.get("username"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            password=user_data.get("password"),
            role=user_data.get("role"),
            age=user_data.get("age")
        )

        for location in user_data["locations"]:
            location, _ = Location.objects.get_or_create(name=location)
            user.location.add(location)

        response: Dict[str, int | str] = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "locations": [
                _location.name for _location in user.location.all()
            ]
        }
        return JsonResponse(response, safe=False,
                            json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    """
    Редактирует запись User
    """
    model = User
    fields = "__all__"

    def patch(self, request, *args, **kwargs) -> JsonResponse:
        super().post(request, *args, **kwargs)
        user_data: Dict[str, str | int | dict] = json.loads(request.body)

        if "username" in user_data:
            self.object.username = user_data["username"]
        if "first_name" in user_data:
            self.object.first_name = user_data["first_name"]
        if "last_name" in user_data:
            self.object.last_name = user_data["last_name"]
        if "age" in user_data:
            self.object.age = user_data["age"]
        if "locations" in user_data:
            self.object.location.all().delete()
            for location in user_data["locations"]:
                location, _ = Location.objects.get_or_create(name=location)
                self.object.location.add(location)

        self.object.save()

        response: Dict[str, int | str | dict] = {
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "locations": [
                _location.name for _location in self.object.location.all()
            ],
            "category": self.object.category
        }
        return JsonResponse(response, safe=False,
                            json_dumps_params={"ensure_ascii": False, "indent": 4})


class UserDeleteView(DestroyAPIView):
    """
    Удаляет запись User по id
    """
    queryset = User.objects.all()
    serializer_class = UserDetailViewSerializer


class LocationViewSet(ModelViewSet):
    """
    Кратко отображает таблицу Местоположения,
    детально отображает запись (выбранную по id),
    создаёт новую запись,
    редактирует запись (выбранную по id),
    удаляет запись (выбранную по id)
    """
    queryset = Location.objects.all()
    serializer_class = LocationViewSetSerializer
