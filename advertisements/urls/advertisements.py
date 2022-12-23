from django.urls import path

from advertisements import views

urlpatterns = [
    path('', views.AdvertisementListView.as_view()),
    path('<int:pk>/', views.AdvertisementDetailView.as_view()),
    path('create/', views.AdvertisementCreateView.as_view()),
    path('<int:pk>/update/', views.AdvertisementUpdateView.as_view()),
    path('<int:pk>/delete/', views.AdvertisementDeleteView.as_view()),
    path('<int:pk>/upload_image/', views.AdvertisementUploadImage.as_view()),
]