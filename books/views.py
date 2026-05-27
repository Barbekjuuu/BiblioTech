from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

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
    """Pełny katalog książek z zaawansowanym wyszukiwaniem i filtrowaniem"""
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
    
    kontekst = {
        'ksiazki': ksiazki,
        'gatunki': gatunki,
        'title': 'Katalog książek',
        'query': query,
        'selected_gatunek': gatunek_id,
        'selected_jezyk': jezyk,
    }
    return render(request, 'katalog.html', kontekst)


def ksiazka_detail(request, pk):
    """Szczegóły jednej książki"""
    ksiazka = get_object_or_404(Ksiazka, pk=pk)
    kontekst = {
        'ksiazka': ksiazka,
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
def rezerwuj_ksiazke(request, egzemplarz_id):
    """Rezerwacja konkretnego egzemplarza"""
    egzemplarz = get_object_or_404(Egzemplarz, id=egzemplarz_id, status='dostepny')
    
    rezerwacja = Rezerwacja.objects.create(
        uzytkownik=request.user,
        egzemplarz=egzemplarz
    )
    
    egzemplarz.status = 'zarezerwowany'
    egzemplarz.save()
    
    messages.success(request, f'Rezerwacja książki "{egzemplarz.ksiazka.tytul}" została pomyślnie utworzona!')
    return redirect('ksiazka_detail', pk=egzemplarz.ksiazka.id)


@login_required
def profile(request):
    """Strona profilu użytkownika z zakładkami"""
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