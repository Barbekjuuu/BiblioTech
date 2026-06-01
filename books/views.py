from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Ksiazka, Gatunek, Egzemplarz, Rezerwacja, RezerwacjaOczekujaca, Powiadomienie
from .forms import UserProfileForm, CustomPasswordChangeForm

# -----------------------------------------------------------------------------
# BiblioTech public views
# -----------------------------------------------------------------------------
# This module contains the core page controllers for the library application:
# - home page with featured books
# - searchable catalog with filters and pagination
# - detailed book view with availability and cart actions
# - user registration, login, logout
# - shopping cart management in session
# - reservation checkout and profile order history
# -----------------------------------------------------------------------------


def home(request):
    """Strona główna biblioteki"""
    ostatnie_ksiazki = Ksiazka.objects.all()[:8]
    kontekst = {
        'ostatnie_ksiazki': ostatnie_ksiazki,
        'title': 'BiblioTech - Biblioteka Online',
    }
    return render(request, 'home.html', kontekst)


def katalog(request):
    """Pełny katalog książek z paginacją.

    Ten widok obsługuje:
    - wyszukiwanie tekstowe
    - filtrowanie po gatunku i języku
    - ustawienie liczby pozycji na stronę
    - przygotowanie danych dostępności egzemplarzy
    """
    ksiazki = Ksiazka.objects.all()
    gatunki = Gatunek.objects.all()
    
    query = request.GET.get('q')
    if query:
        ksiazki = ksiazki.filter(
            Q(tytul__icontains=query) | 
            Q(opis__icontains=query) | 
            Q(autor__imie_nazwisko__icontains=query) |
            Q(gatunek__nazwa__icontains=query)
        )
    
    gatunek_id = request.GET.get('gatunek')
    if gatunek_id:
        ksiazki = ksiazki.filter(gatunek_id=gatunek_id)
    
    jezyk = request.GET.get('jezyk')
    if jezyk:
        ksiazki = ksiazki.filter(jezyk=jezyk)
    
    # Przygotowanie danych dla szablonu
    ksiazki_z_danymi = []
    for ksiazka in ksiazki:
        # Przygotowujemy dodatkowe dane dla każdej książki:
        # - liczbę dostępnych egzemplarzy
        # - pierwszy dostępny egzemplarz do szybkiej akcji wypożyczenia
        dostepne = ksiazka.egzemplarze.filter(status='dostepny')
        available_count = dostepne.count()
        first_available_id = dostepne.first().id if dostepne.exists() else None
        
        ksiazka.available_count = available_count
        ksiazka.first_available_id = first_available_id
        ksiazki_z_danymi.append(ksiazka)
    
    # PAGINACJA
    per_page = request.GET.get('per_page', 12)
    try:
        per_page = int(per_page)
    except:
        per_page = 12
    
    paginator = Paginator(ksiazki_z_danymi, per_page)
    page_number = request.GET.get('page')
    try:
        ksiazki_page = paginator.get_page(page_number)
    except PageNotAnInteger:
        ksiazki_page = paginator.get_page(1)
    except EmptyPage:
        ksiazki_page = paginator.get_page(paginator.num_pages)
    
    kontekst = {
        'ksiazki': ksiazki_page,
        'gatunki': gatunki,
        'title': 'Katalog książek',
        'query': query,
        'selected_gatunek': gatunek_id,
        'selected_jezyk': jezyk,
        'per_page': per_page,
        'per_page_options': [6, 12, 24],
        'paginator': paginator,
    }
    return render(request, 'katalog.html', kontekst)


def ksiazka_detail(request, pk):
    """Szczegóły jednej książki.

    Widok pokazuje pełne dane książki wraz z liczbą dostępnych egzemplarzy.
    Jeśli egzemplarze są dostępne, udostępnia szybki przycisk dodania do koszyka.
    """
    ksiazka = get_object_or_404(Ksiazka, pk=pk)
    
    # Poprawne liczenie dostępnych egzemplarzy
    dostepne = ksiazka.egzemplarze.filter(status='dostepny')
    available_count = dostepne.count()
    first_available_id = dostepne.first().id if dostepne.exists() else None
    
    kontekst = {
        'ksiazka': ksiazka,
        'available_count': available_count,
        'first_available_id': first_available_id,
        'title': ksiazka.tytul,
    }
    return render(request, 'ksiazka_detail.html', kontekst)


def register(request):
    """Rejestracja nowego użytkownika"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Konto zostało utworzone pomyślnie!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm
    
    def get_success_url(self):
        return '/'


class CustomLogoutView(LogoutView):
    next_page = 'home'
    http_method_names = ['get', 'post']


def notify_next_waiting_user(ksiazka):
    """Tworzy powiadomienie dla pierwszej oczekującej rezerwacji na daną książkę."""
    zgloszenie = RezerwacjaOczekujaca.objects.filter(
        ksiazka=ksiazka,
        aktywna=True,
        powiadomiony=False
    ).order_by('data_zgloszenia').first()

    if not zgloszenie:
        return

    Powiadomienie.objects.create(
        uzytkownik=zgloszenie.uzytkownik,
        tytul=f'Książka "{ksiazka.tytul}" jest dostępna',
        tresc=(
            f'Książka "{ksiazka.tytul}" jest teraz dostępna. '
            'Przejdź do jej strony, aby wypożyczyć lub dodać do koszyka.'
        ),
        link=reverse('ksiazka_detail', args=[ksiazka.id])
    )
    zgloszenie.powiadomiony = True
    zgloszenie.save()


@login_required
def dodaj_do_koszyka(request, egzemplarz_id):
    """Dodaje egzemplarz do koszyka (sesja)."""
    egzemplarz = get_object_or_404(Egzemplarz, id=egzemplarz_id, status='dostepny')
    
    # Koszyk jest przechowywany w sesji przeglądarki użytkownika.
    # To podejście pozwala zachować stan przed zatwierdzeniem wypożyczenia,
    # a jednocześnie nie wymaga tworzenia osobnego modelu koszyka.
    koszyk = request.session.get('koszyk', [])
    if egzemplarz_id not in koszyk:
        koszyk.append(egzemplarz_id)
        request.session['koszyk'] = koszyk
        messages.success(request, f'Książka "{egzemplarz.ksiazka.tytul}" dodana do koszyka.')
    else:
        messages.info(request, 'Ta książka jest już w koszyku.')
    
    return redirect('ksiazka_detail', pk=egzemplarz.ksiazka.id)


@login_required
def zarezerwuj_ksiazke(request, ksiazka_id):
    """Tworzy zgłoszenie oczekującej rezerwacji dla książki."""
    ksiazka = get_object_or_404(Ksiazka, id=ksiazka_id)
    dostepne = ksiazka.egzemplarze.filter(status='dostepny').exists()

    if dostepne:
        messages.info(request, 'Ta książka jest dostępna. Dodaj ją do koszyka, aby wypożyczyć.')
        return redirect('ksiazka_detail', pk=ksiazka.id)

    istnieje = RezerwacjaOczekujaca.objects.filter(uzytkownik=request.user, ksiazka=ksiazka, aktywna=True).exists()
    if istnieje:
        messages.info(request, 'Masz już oczekującą rezerwację dla tej książki.')
        return redirect('ksiazka_detail', pk=ksiazka.id)

    RezerwacjaOczekujaca.objects.create(
        uzytkownik=request.user,
        ksiazka=ksiazka
    )
    messages.success(request, 'Zgłoszono oczekującą rezerwację. Otrzymasz powiadomienie, gdy egzemplarz będzie dostępny.')
    return redirect('ksiazka_detail', pk=ksiazka.id)


@login_required
def koszyk(request):
    """Osobna strona koszyka"""
    koszyk_ids = request.session.get('koszyk', [])
    egzemplarze = Egzemplarz.objects.filter(id__in=koszyk_ids)
    
    kontekst = {
        'egzemplarze': egzemplarze,
        'title': 'Koszyk rezerwacji',
    }
    return render(request, 'koszyk.html', kontekst)


@login_required
def zatwierdz_koszyk(request):
    """Zatwierdza koszyk i przenosi do Moich wypożyczeń."""
    koszyk_ids = request.session.get('koszyk', [])

    try:
        with transaction.atomic():
            # Przy zatwierdzaniu koszyka tworzymy rezerwacje dla wszystkich dodanych egzemplarzy.
            # Transakcja gwarantuje, że żaden egzemplarz nie zostanie zarezerwowany dwukrotnie.
            for egz_id in koszyk_ids:
                egzemplarz = get_object_or_404(
                    Egzemplarz.objects.select_for_update(),
                    id=egz_id,
                    status='dostepny'
                )
                Rezerwacja.objects.create(
                    uzytkownik=request.user,
                    egzemplarz=egzemplarz
                )
                egzemplarz.status = 'zarezerwowany'
                egzemplarz.save()
    except Http404:
        messages.error(request, 'One or more books in your cart are no longer available. Please refresh the cart.')
        return redirect('koszyk')

    request.session['koszyk'] = []
    messages.success(request, 'Wypożyczenie zostało zatwierdzone!')
    return redirect('profile')


@login_required
def profile(request):
    """Strona profilu użytkownika."""
    tab = request.GET.get('tab', 'rezerwacje')
    rezerwacje = request.user.rezerwacje.filter(data_zwrotu__isnull=True).order_by('-data_rezerwacji')
    historia_rezerwacji = request.user.rezerwacje.filter(data_zwrotu__isnull=False).order_by('-data_zwrotu')
    rezerwacje_oczekujace = request.user.oczekujace_rezerwacje.filter(aktywna=True).order_by('-data_zgloszenia')
    powiadomienia = request.user.powiadomienia.order_by('-utworzone')

    profile_form = UserProfileForm(instance=request.user)
    password_form = CustomPasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'profile':
            tab = 'dane'
            profile_form = UserProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Twoje dane osobowe zostały zaktualizowane.')
                return redirect(f"{reverse('profile')}?tab=dane")

        elif form_type == 'password':
            tab = 'haslo'
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Hasło zostało pomyślnie zmienione.')
                return redirect(f"{reverse('profile')}?tab=haslo")

    kontekst = {
        'rezerwacje': rezerwacje,
        'historia_rezerwacji': historia_rezerwacji,
        'rezerwacje_oczekujace': rezerwacje_oczekujace,
        'powiadomienia': powiadomienia,
        'title': 'Mój Profil',
        'active_tab': tab,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'profile.html', kontekst)


@login_required
def anuluj_rezerwacje(request, rezerwacja_id):
    """Anulowanie rezerwacji"""
    rezerwacja = get_object_or_404(Rezerwacja, id=rezerwacja_id, uzytkownik=request.user)
    egzemplarz = rezerwacja.egzemplarz
    egzemplarz.status = 'dostepny'
    egzemplarz.save()
    notify_next_waiting_user(egzemplarz.ksiazka)
    rezerwacja.delete()
    
    messages.success(request, 'Rezerwacja została pomyślnie anulowana.')
    return redirect('profile')


@login_required
def zwroc_rezerwacje(request, rezerwacja_id):
    """Obsługa zwrotu rezerwacji i przywrócenie egzemplarza do dostępnych."""
    rezerwacja = get_object_or_404(Rezerwacja, id=rezerwacja_id, uzytkownik=request.user, data_zwrotu__isnull=True)
    egzemplarz = rezerwacja.egzemplarz
    egzemplarz.status = 'dostepny'
    egzemplarz.save()

    rezerwacja.data_zwrotu = timezone.now()
    rezerwacja.save()

    notify_next_waiting_user(egzemplarz.ksiazka)
    messages.success(request, 'Książka została zwrócona i jest ponownie dostępna.')
    return redirect('profile')


@login_required
def oznacz_powiadomienie_przeczytane(request, powiadomienie_id):
    """Oznacza powiadomienie jako przeczytane i przekierowuje użytkownika."""
    powiadomienie = get_object_or_404(Powiadomienie, id=powiadomienie_id, uzytkownik=request.user)
    powiadomienie.przeczytane = True
    powiadomienie.save()

    if powiadomienie.link:
        return redirect(powiadomienie.link)
    return redirect('profile')


@login_required
def oznacz_wszystkie_powiadomienia_przeczytane(request):
    """Oznacza wszystkie powiadomienia użytkownika jako przeczytane."""
    if request.method == 'POST':
        request.user.powiadomienia.filter(przeczytane=False).update(przeczytane=True)
        messages.success(request, 'Wszystkie powiadomienia zostały oznaczone jako przeczytane.')
    return redirect(f"{reverse('profile')}?tab=powiadomienia")


# ====================== NOWA FUNKCJA ======================

@login_required
def usun_z_koszyka(request, egzemplarz_id):
    """Usuwa egzemplarz z koszyka"""
    koszyk = request.session.get('koszyk', [])
    if egzemplarz_id in koszyk:
        koszyk.remove(egzemplarz_id)
        request.session['koszyk'] = koszyk
        messages.success(request, 'Książka została usunięta z koszyka.')
    return redirect('koszyk')