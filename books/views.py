from django.shortcuts import render, get_object_or_404
from .models import Ksiazka, Gatunek
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    """Strona główna biblioteki"""
    ostatnie_ksiazki = Ksiazka.objects.all()[:8]  # ostatnie 8 książek
    kontekst = {
        'ostatnie_ksiazki': ostatnie_ksiazki,
        'title': 'BiblioTech - Biblioteka Online',
    }
    return render(request, 'home.html', kontekst)


def katalog(request):
    """Pełny katalog książek z możliwością filtrowania"""
    ksiazki = Ksiazka.objects.all()
    gatunki = Gatunek.objects.all()
    
    # Filtrowanie po gatunku
    gatunek_id = request.GET.get('gatunek')
    if gatunek_id:
        ksiazki = ksiazki.filter(gatunek_id=gatunek_id)
    
    kontekst = {
        'ksiazki': ksiazki,
        'gatunki': gatunki,
        'title': 'Katalog książek',
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