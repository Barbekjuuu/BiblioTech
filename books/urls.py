from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('katalog/', views.katalog, name='katalog'),
    path('ksiazka/<int:pk>/', views.ksiazka_detail, name='ksiazka_detail'),
    
    # Uwierzytelnianie
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Rezerwacja książki
    path('rezerwuj/<int:egzemplarz_id>/', views.rezerwuj_ksiazke, name='rezerwuj_ksiazke'),
]