from django.shortcuts import render, get_object_or_404
from .models import Ksiazka, Gatunek
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Egzemplarz, Rezerwacja
from django.db.models import Q


def home(request):
    """Strona główna biblioteki"""
    ostatnie_ksiazki = Ksiazka.objects.all()[:8]  # ostatnie 8 książek
    kontekst = {
        'ostatnie_ksiazki': ostatnie_ksiazki,
        'title': 'BiblioTech - Biblioteka Online',
    }
    return render(request, 'home.html', kontekst)


def katalog(request):
    """Pełny katalog książek z zaawansowanym wyszukiwaniem i filtrowaniem"""
    ksiazki = Ksiazka.objects.all()
    gatunki = Gatunek.objects.all()
    
    # Wyszukiwanie tekstowe (po tytule, autorze, opisie, gatunku)
    query = request.GET.get('q')
    if query:
        ksiazki = ksiazki.filter(
            Q(tytul__icontains=query) | 
            Q(opis__icontains=query) | 
            Q(autor__imie_nazwisko__icontains=query) |
            Q(gatunek__nazwa__icontains=query)
        )
    
    # Filtr po gatunku
    gatunek_id = request.GET.get('gatunek')
    if gatunek_id:
        ksiazki = ksiazki.filter(gatunek_id=gatunek_id)
    
    # FILTR PO JĘZYKU
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

# Widok logowania
class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm
    
    def get_success_url(self):
        return '/'

# Widok wylogowania
class CustomLogoutView(LogoutView):
    next_page = 'home'
    http_method_names = ['get', 'post']  

@login_required
def rezerwuj_ksiazke(request, egzemplarz_id):
    """Rezerwacja konkretnego egzemplarza"""
    egzemplarz = get_object_or_404(Egzemplarz, id=egzemplarz_id, status='dostepny')
    
    # Tworzymy rezerwację
    rezerwacja = Rezerwacja.objects.create(
        uzytkownik=request.user,
        egzemplarz=egzemplarz
    )
    
    # Zmiana statusu egzemplarza
    egzemplarz.status = 'zarezerwowany'
    egzemplarz.save()
    
    messages.success(request, f'Rezerwacja książki "{egzemplarz.ksiazka.tytul}" została pomyślnie utworzona!')
    return redirect('ksiazka_detail', pk=egzemplarz.ksiazka.id)

@login_required
def moje_rezerwacje(request):
    """Wyświetla rezerwacje zalogowanego użytkownika"""
    rezerwacje = Rezerwacja.objects.filter(uzytkownik=request.user).order_by('-data_rezerwacji')
    
    kontekst = {
        'rezerwacje': rezerwacje,
        'title': 'Moje rezerwacje',
    }
    return render(request, 'moje_rezerwacje.html', kontekst)