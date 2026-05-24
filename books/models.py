from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Autor(models.Model):
    """Model autora książki"""
    imie_nazwisko = models.CharField(max_length=200)
    zdjecie = models.ImageField(upload_to='autorzy/', blank=True, null=True)

    def __str__(self):
        return self.imie_nazwisko

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autorzy"


class Gatunek(models.Model):
    """Gatunek literacki"""
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Gatunek"
        verbose_name_plural = "Gatunki"


class Ksiazka(models.Model):
    """Główny model książki"""
    tytul = models.CharField(max_length=300)
    opis = models.TextField(blank=True)
    data_wydania = models.DateField(null=True, blank=True)
    okladka = models.ImageField(upload_to='okladki/', blank=True, null=True)
    
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='ksiazki')
    gatunek = models.ForeignKey(Gatunek, on_delete=models.SET_NULL, null=True, related_name='ksiazki')

    def __str__(self):
        return self.tytul

    class Meta:
        verbose_name = "Książka"
        verbose_name_plural = "Książki"


class Egzemplarz(models.Model):
    """Konkretny egzemplarz książki w bibliotece"""
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
    """Rezerwacja książki przez użytkownika"""
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rezerwacje')
    egzemplarz = models.ForeignKey(Egzemplarz, on_delete=models.CASCADE, related_name='rezerwacje')
    
    data_rezerwacji = models.DateTimeField(auto_now_add=True)
    data_waznosci = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.data_waznosci:
            self.data_waznosci = self.data_rezerwacji + timedelta(weeks=2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rezerwacja: {self.egzemplarz} dla {self.uzytkownik}"

    class Meta:
        verbose_name = "Rezerwacja"
        verbose_name_plural = "Rezerwacje"