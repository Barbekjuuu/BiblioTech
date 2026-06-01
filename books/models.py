from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Modele w tej aplikacji odzwierciedlają podstawową strukturę systemu bibliotecznego:
# - Autor: informacje o autorze
# - Gatunek: kategoryzacja książki
# - Ksiazka: dane książki i relacje do autora/gatunku
# - Egzemplarz: pojedynczy egzemplarz książki w bibliotece
# - Rezerwacja: aktywny zapis użytkownika na konkretny egzemplarz


class Autor(models.Model):
    """Model autora książki.

    Autor zawiera imię i nazwisko oraz opcjonalne zdjęcie.
    Ten model jest powiązany z modelem `Ksiazka` relacją wiele-do-jednego.
    """
    imie_nazwisko = models.CharField(max_length=200)
    zdjecie = models.ImageField(upload_to='autorzy/', blank=True, null=True)

    def __str__(self):
        return self.imie_nazwisko

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autorzy"


class Gatunek(models.Model):
    """Gatunek literacki.

    Gatunek jest prostym słownikiem, który umożliwia filtrowanie książek.
    """
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Gatunek"
        verbose_name_plural = "Gatunki"


class Ksiazka(models.Model):
    """Główny model książki.

    Model przechowuje dane książki, w tym: tytuł, opis, datę wydania,
    okładkę, język oraz relacje do autora i gatunku.
    """
    JEZYK_CHOICES = [
        ('pl', 'Polski'),
        ('en', 'Angielski'),
        ('de', 'Niemiecki'),
        ('fr', 'Francuski'),
        ('es', 'Hiszpański'),
        ('it', 'Włoski'),
        ('ru', 'Rosyjski'),
        ('inne', 'Inny'),
    ]
    
    tytul = models.CharField(max_length=300)
    opis = models.TextField(blank=True)
    data_wydania = models.DateField(null=True, blank=True)
    okladka = models.ImageField(upload_to='okladki/', blank=True, null=True)
    jezyk = models.CharField(max_length=10, choices=JEZYK_CHOICES, default='pl')
    
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='ksiazki')
    gatunek = models.ForeignKey(Gatunek, on_delete=models.SET_NULL, null=True, related_name='ksiazki')
    def okladka_url(self):
        """Zwraca URL okładki lub domyślny obrazek.

        W widokach i szablonach używamy tej metody, aby zawsze mieć bezpieczny
        adres URL do wyświetlenia. Jeśli okładka nie jest załadowana, zwracany jest
        stały zasób statyczny.
        """
        if self.okladka:
            return self.okladka.url
        return '/static/images/cover.png'  # domyślna okładka
    def __str__(self):
        return self.tytul

    class Meta:
        verbose_name = "Książka"
        verbose_name_plural = "Książki"


class Egzemplarz(models.Model):
    """Konkretny egzemplarz książki w bibliotece.

    Ten model reprezentuje pojedynczy dostępny lub wypożyczony egzemplarz.
    Umożliwia zarządzanie stanem egzemplarza w procesie rezerwacji.
    """
    STATUS_CHOICES = [
        ('dostepny', 'Dostępny'),
        ('wypozyczony', 'Wypożyczony'),
        ('zarezerwowany', 'Zarezerwowany'),
    ]
    
    ksiazka = models.ForeignKey(Ksiazka, on_delete=models.CASCADE, related_name='egzemplarze')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='dostepny')

    def __str__(self):
        return f"{self.ksiazka.tytul} - {self.get_status_display()}"

    class Meta:
        verbose_name = "Egzemplarz"
        verbose_name_plural = "Egzemplarze"


class Rezerwacja(models.Model):
    """Rezerwacja książki przez użytkownika.

    Rezerwacja łączy użytkownika z egzemplarzem na okres 2 tygodni.
    W momencie zapisu ustawiane są daty rezerwacji i ważności.
    """
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rezerwacje')
    egzemplarz = models.ForeignKey(Egzemplarz, on_delete=models.CASCADE, related_name='rezerwacje')
    
    data_rezerwacji = models.DateTimeField(auto_now_add=True)
    data_waznosci = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Ustawiamy datę rezerwacji jeśli nie jest ustawiona
        if not self.data_rezerwacji:
            self.data_rezerwacji = timezone.now()
        
        # Obliczamy datę ważności (2 tygodnie)
        if not self.data_waznosci:
            self.data_waznosci = self.data_rezerwacji + timedelta(weeks=2)
        
        super().save(*args, **kwargs)    

    def __str__(self):
        return f"Rezerwacja: {self.egzemplarz} dla {self.uzytkownik}"

    class Meta:
        verbose_name = "Rezerwacja"
        verbose_name_plural = "Rezerwacje"