from django.contrib import admin
from .models import Autor, Gatunek, Ksiazka, Egzemplarz, Rezerwacja


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('imie_nazwisko', 'zdjecie')
    search_fields = ('imie_nazwisko',)
    list_per_page = 20


@admin.register(Gatunek)
class GatunekAdmin(admin.ModelAdmin):
    list_display = ('nazwa',)
    search_fields = ('nazwa',)


class EgzemplarzInline(admin.TabularInline):
    model = Egzemplarz
    extra = 1


@admin.register(Ksiazka)
class KsiazkaAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'autor', 'gatunek', 'data_wydania', 'liczba_egzemplarzy')
    list_filter = ('gatunek', 'data_wydania')
    search_fields = ('tytul', 'opis')
    inlines = [EgzemplarzInline]

    def liczba_egzemplarzy(self, obj):
        return obj.egzemplarze.count()
    liczba_egzemplarzy.short_description = 'Liczba egzemplarzy'


@admin.register(Egzemplarz)
class EgzemplarzAdmin(admin.ModelAdmin):
    list_display = ('ksiazka', 'status')
    list_filter = ('status',)
    search_fields = ('ksiazka__tytul',)


@admin.register(Rezerwacja)
class RezerwacjaAdmin(admin.ModelAdmin):
    list_display = ('uzytkownik', 'egzemplarz', 'data_rezerwacji', 'data_waznosci', 'czy_wazna')
    list_filter = ('data_rezerwacji',)
    search_fields = ('uzytkownik__username', 'egzemplarz__ksiazka__tytul')
    readonly_fields = ('data_rezerwacji',)

    def czy_wazna(self, obj):
        return obj.data_waznosci > timezone.now()
    czy_wazna.boolean = True
    czy_wazna.short_description = 'Czy ważna?'