from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Ksiazka, Gatunek, Egzemplarz, Rezerwacja


def home(request):
    """Strona główna biblioteki"""
    ostatnie_ksiazki = Ksiazka.objects.all()[:8]
    kontekst = {
        'ostatnie_ksiazki': ostatnie_ksiazki,
        'title': 'BiblioTech - Biblioteka Online',
    }
    return render(request, 'home.html', kontekst)


def katalog(request):
    """Pełny katalog książek z paginacją"""
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
    """Szczegóły jednej książki"""
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


@login_required
def dodaj_do_koszyka(request, egzemplarz_id):
    """Dodaje egzemplarz do koszyka (sesja)"""
    egzemplarz = get_object_or_404(Egzemplarz, id=egzemplarz_id, status='dostepny')
    
    koszyk = request.session.get('koszyk', [])
    if egzemplarz_id not in koszyk:
        koszyk.append(egzemplarz_id)
        request.session['koszyk'] = koszyk
        messages.success(request, f'Książka "{egzemplarz.ksiazka.tytul}" dodana do koszyka.')
    else:
        messages.info(request, 'Ta książka jest już w koszyku.')
    
    return redirect('ksiazka_detail', pk=egzemplarz.ksiazka.id)


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
    """Zatwierdza koszyk i przenosi do Moich wypożyczeń"""
    koszyk_ids = request.session.get('koszyk', [])
    
    for egz_id in koszyk_ids:
        egzemplarz = get_object_or_404(Egzemplarz, id=egz_id, status='dostepny')
        Rezerwacja.objects.create(
            uzytkownik=request.user,
            egzemplarz=egzemplarz
        )
        egzemplarz.status = 'zarezerwowany'
        egzemplarz.save()
    
    request.session['koszyk'] = []
    messages.success(request, 'Wypożyczenie zostało zatwierdzone!')
    return redirect('profile')


@login_required
def profile(request):
    """Strona profilu użytkownika"""
    tab = request.GET.get('tab', 'rezerwacje')
    rezerwacje = request.user.rezerwacje.all().order_by('-data_rezerwacji')
    
    kontekst = {
        'rezerwacje': rezerwacje,
        'title': 'Mój Profil',
        'active_tab': tab,
    }
    return render(request, 'profile.html', kontekst)


@login_required
def anuluj_rezerwacje(request, rezerwacja_id):
    """Anulowanie rezerwacji"""
    rezerwacja = get_object_or_404(Rezerwacja, id=rezerwacja_id, uzytkownik=request.user)
    egzemplarz = rezerwacja.egzemplarz
    egzemplarz.status = 'dostepny'
    egzemplarz.save()
    rezerwacja.delete()
    
    messages.success(request, 'Rezerwacja została pomyślnie anulowana.')
    return redirect('profile')