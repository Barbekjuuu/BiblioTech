from django.contrib import admin
from .models import Autor, Gatunek, Ksiazka, Egzemplarz, Rezerwacja


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('imie_nazwisko',)
    search_fields = ('imie_nazwisko',)


@admin.register(Gatunek)
class GatunekAdmin(admin.ModelAdmin):
    list_display = ('nazwa',)
    search_fields = ('nazwa',)


@admin.register(Ksiazka)
class KsiazkaAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'autor', 'gatunek', 'data_wydania')
    list_filter = ('gatunek', 'data_wydania')
    search_fields = ('tytul', 'opis')
   


@admin.register(Egzemplarz)
class EgzemplarzAdmin(admin.ModelAdmin):
    list_display = ('ksiazka', 'status')
    list_filter = ('status',)
    search_fields = ('ksiazka__tytul',)


@admin.register(Rezerwacja)
class RezerwacjaAdmin(admin.ModelAdmin):
    list_display = ('uzytkownik', 'egzemplarz', 'data_rezerwacji', 'data_waznosci')
    list_filter = ('data_rezerwacji',)
    search_fields = ('uzytkownik__username', 'egzemplarz__ksiazka__tytul')