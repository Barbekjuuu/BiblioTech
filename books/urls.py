from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('katalog/', views.katalog, name='katalog'),
    path('ksiazka/<int:pk>/', views.ksiazka_detail, name='ksiazka_detail'),
]