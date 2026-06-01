from django.contrib import admin
from django.utils.html import format_html
from .models import Autor, Gatunek, Ksiazka, Egzemplarz, Rezerwacja, RezerwacjaOczekujaca

class EgzemplarzInline(admin.TabularInline):
    model = Egzemplarz
    extra = 1

    # Egzemplarze wyświetlane inline w edycji książki.
    # Dzięki temu administrator może dodać lub zmienić egzemplarze bez opuszczania formularza książki.

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('imie_nazwisko', 'zdjecie_preview')
    search_fields = ('imie_nazwisko',)

    def zdjecie_preview(self, obj):
        if obj.zdjecie:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;" />', obj.zdjecie.url)
        return "Brak zdjęcia"
    zdjecie_preview.short_description = "Zdjęcie"

@admin.register(Gatunek)
class GatunekAdmin(admin.ModelAdmin):
    list_display = ('nazwa',)
    search_fields = ('nazwa',)

@admin.register(Ksiazka)
class KsiazkaAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'autor', 'gatunek', 'jezyk', 'data_wydania', 'okladka_preview')
    list_filter = ('gatunek', 'jezyk', 'data_wydania')
    search_fields = ('tytul', 'opis', 'autor__imie_nazwisko')
    inlines = [EgzemplarzInline]

    # Administracyjny panel książki pokazuje listę pól w tabeli,
    # umożliwia szybkie filtrowanie i wyszukiwanie oraz podgląd okładki.

    def okladka_preview(self, obj):
        if obj.okladka:
            return format_html('<img src="{}" width="60" height="80" style="object-fit:cover;" />', obj.okladka.url)
        return "Brak okładki"
    okladka_preview.short_description = "Okładka"

@admin.register(Egzemplarz)
class EgzemplarzAdmin(admin.ModelAdmin):
    list_display = ('ksiazka', 'status')
    list_filter = ('status',)

@admin.register(Rezerwacja)
class RezerwacjaAdmin(admin.ModelAdmin):
    list_display = ('uzytkownik', 'egzemplarz', 'data_rezerwacji', 'data_waznosci')
    list_filter = ('data_rezerwacji',)

    # Rezerwacje można szybko przeglądać w adminie, co ułatwia obsługę biblioteki.

@admin.register(RezerwacjaOczekujaca)
class RezerwacjaOczekujacaAdmin(admin.ModelAdmin):
    list_display = ('uzytkownik', 'ksiazka', 'aktywna', 'data_zgloszenia')
    list_filter = ('aktywna', 'data_zgloszenia')
    search_fields = ('uzytkownik__username', 'ksiazka__tytul')