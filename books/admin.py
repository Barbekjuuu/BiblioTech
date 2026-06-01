from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Autor, Gatunek, Ksiazka, Egzemplarz, Rezerwacja, RezerwacjaOczekujaca, Powiadomienie
from django import forms
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth import get_user_model

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
    raw_id_fields = ('uzytkownik', 'egzemplarz')
    actions = ('mark_returned',)
    date_hierarchy = 'data_rezerwacji'

    # Rezerwacje można szybko przeglądać w adminie, co ułatwia obsługę biblioteki.

    def save_model(self, request, obj, form, change):
        # Przy zapisie rezerwacji, upewniamy się, że status egzemplarza jest zsynchronizowany.
        super().save_model(request, obj, form, change)
        egz = obj.egzemplarz
        if egz:
            if obj.data_zwrotu:
                egz.status = 'dostepny'
            else:
                egz.status = 'zarezerwowany'
            egz.save()

    def mark_returned(self, request, queryset):
        """Akcja admina: oznacz zaznaczone rezerwacje jako zwrócone."""
        now = timezone.now()
        updated = 0
        for r in queryset.filter(data_zwrotu__isnull=True):
            r.data_zwrotu = now
            r.save()
            egz = r.egzemplarz
            egz.status = 'dostepny'
            egz.save()
            updated += 1
        self.message_user(request, f"{updated} rezerwacji oznaczono jako zwrócone.")
    mark_returned.short_description = 'Oznacz zaznaczone rezerwacje jako zwrócone'

    # Custom admin view to create a reservation for a user (staff workflow)
    class ReserveForUserForm(forms.Form):
        egzemplarz = forms.ModelChoiceField(queryset=Egzemplarz.objects.select_related('ksiazka'), label='Egzemplarz')
        email = forms.EmailField(label='Email klienta')
        first_name = forms.CharField(label='Imię klienta', required=False)
        last_name = forms.CharField(label='Nazwisko klienta', required=False)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create_for_user/', self.admin_site.admin_view(self.create_for_user_view), name='books_rezerwacja_create_for_user'),
        ]
        return custom_urls + urls

    def create_for_user_view(self, request):
        """Admin view: allow staff to reserve a specific copy for a client by email/name."""
        if request.method == 'POST':
            form = self.ReserveForUserForm(request.POST)
            if form.is_valid():
                egz = form.cleaned_data['egzemplarz']
                email = form.cleaned_data['email']
                # walidacja statusu egzemplarza
                if egz.status != 'dostepny':
                    form.add_error('egzemplarz', 'Wybrany egzemplarz nie jest dostępny do rezerwacji.')
                else:
                    # proceed to create or get user and reservation
                    first = form.cleaned_data.get('first_name') or ''
                    last = form.cleaned_data.get('last_name') or ''
                    User = get_user_model()
                    username = email.split('@')[0]
                    user, created = User.objects.get_or_create(email=email, defaults={'username': username, 'first_name': first, 'last_name': last})
                    if created:
                        user.set_unusable_password()
                        user.save()

                    # create reservation
                    rezerwacja = Rezerwacja.objects.create(uzytkownik=user, egzemplarz=egz)
                    egz.status = 'zarezerwowany'
                    egz.save()
                    self.message_user(request, f'Rezerwacja utworzona dla {email}.')
                    return HttpResponseRedirect(reverse('admin:books_rezerwacja_changelist'))
                # if form invalid, fall through and render form with errors
        else:
            form = self.ReserveForUserForm()

        context = dict(self.admin_site.each_context(request), form=form, opts=self.model._meta)
        return TemplateResponse(request, 'admin/reserve_for_user.html', context)

@admin.register(RezerwacjaOczekujaca)
class RezerwacjaOczekujacaAdmin(admin.ModelAdmin):
    list_display = ('uzytkownik', 'ksiazka', 'aktywna', 'powiadomiony', 'data_zgloszenia')
    list_filter = ('aktywna', 'powiadomiony', 'data_zgloszenia')
    search_fields = ('uzytkownik__username', 'ksiazka__tytul')
    actions = ('mark_notified','deactivate_requests')

    def mark_notified(self, request, queryset):
        updated = queryset.update(powiadomiony=True)
        self.message_user(request, f"{updated} zgłoszeń oznaczono jako powiadomione.")
    mark_notified.short_description = 'Oznacz jako powiadomione'

    def deactivate_requests(self, request, queryset):
        updated = queryset.update(aktywna=False)
        self.message_user(request, f"{updated} zgłoszeń dezaktywowano.")
    deactivate_requests.short_description = 'Dezaktywuj zaznaczone zgłoszenia'


@admin.register(Powiadomienie)
class PowiadomienieAdmin(admin.ModelAdmin):
    list_display = ('uzytkownik', 'tytul', 'przeczytane', 'utworzone')
    list_filter = ('przeczytane', 'utworzone')
    search_fields = ('uzytkownik__username', 'tytul')
    actions = ('mark_read','mark_unread')

    def mark_read(self, request, queryset):
        updated = queryset.update(przeczytane=True)
        self.message_user(request, f"{updated} powiadomień oznaczono jako przeczytane.")
    mark_read.short_description = 'Oznacz jako przeczytane'

    def mark_unread(self, request, queryset):
        updated = queryset.update(przeczytane=False)
        self.message_user(request, f"{updated} powiadomień oznaczono jako nieprzeczytane.")
    mark_unread.short_description = 'Oznacz jako nieprzeczytane'
