from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User, Location
from users.serializers import LocationViewSetSerializer, UserDetailViewSerializer, \
    UserListViewSerializer, UserCreateViewSerializer, UserUpdateViewSerializer


class UserListView(ListAPIView):
    """
    Кратко отображает таблицу Пользователи
    """
    queryset = User.objects.all().order_by("username")
    serializer_class = UserListViewSerializer


class UserDetailView(RetrieveAPIView):
    """
    Делает выборку записи из таблицы Пользователи по id
    """
    queryset = User.objects.all()
    serializer_class = UserDetailViewSerializer


class UserCreateView(CreateAPIView):
    """
    Cоздаёт новую запись User по id
    """
    queryset = User.objects.all()
    serializer_class = UserCreateViewSerializer


class UserUpdateView(UpdateAPIView):
    """
    Редактирует запись User по id
    """
    queryset = User.objects.all()
    serializer_class = UserUpdateViewSerializer


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
