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
    
    # Koszyk i wypożyczenia
    path('koszyk/', views.koszyk, name='koszyk'),
    path('koszyk/dodaj/<int:egzemplarz_id>/', views.dodaj_do_koszyka, name='dodaj_do_koszyka'),
    path('koszyk/usun/<int:egzemplarz_id>/', views.usun_z_koszyka, name='usun_z_koszyka'),
    path('koszyk/zatwierdz/', views.zatwierdz_koszyk, name='zatwierdz_koszyk'),
    
    # Profil i zarządzanie
    path('profil/', views.profile, name='profile'),
    path('powiadomienie/przeczytaj/<int:powiadomienie_id>/', views.oznacz_powiadomienie_przeczytane, name='oznacz_powiadomienie_przeczytane'),
    path('powiadomienie/oznacz-wszystkie/', views.oznacz_wszystkie_powiadomienia_przeczytane, name='oznacz_wszystkie_powiadomienia_przeczytane'),
    path('rezerwacja/zwroc/<int:rezerwacja_id>/', views.zwroc_rezerwacje, name='zwroc_rezerwacje'),
    path('rezerwacja/oczekujaca/anuluj/<int:oczekujaca_id>/', views.anuluj_rezerwacje_oczekujaca, name='anuluj_rezerwacje_oczekujaca'),
    path('ksiazka/rezerwuj/<int:ksiazka_id>/', views.zarezerwuj_ksiazke, name='zarezerwuj_ksiazke'),
    path('rezerwacja/anuluj/<int:rezerwacja_id>/', views.anuluj_rezerwacje, name='anuluj_rezerwacje'),
]