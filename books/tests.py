from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Autor, Gatunek, Ksiazka, Egzemplarz, Rezerwacja
from django.urls import reverse
from django.utils import timezone


class BiblioTechTests(TestCase):

    def setUp(self):
        """Przygotowanie danych testowych"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        self.autor = Autor.objects.create(imie_nazwisko='Jan Kowalski')
        self.gatunek = Gatunek.objects.create(nazwa='Fantastyka')
        
        self.ksiazka = Ksiazka.objects.create(
            tytul='Testowa Książka',
            opis='Opis testowej książki',
            autor=self.autor,
            gatunek=self.gatunek
        )
        self.egzemplarz = Egzemplarz.objects.create(
            ksiazka=self.ksiazka, 
            status='dostepny'
        )

    def test_model_autor(self):
        """Test modelu Autor"""
        self.assertEqual(str(self.autor), 'Jan Kowalski')

    def test_model_ksiazka(self):
        """Test modelu Książka"""
        self.assertEqual(str(self.ksiazka), 'Testowa Książka')

    def test_rezerwacja(self):
        """Test tworzenia rezerwacji"""
        rezerwacja = Rezerwacja.objects.create(
            uzytkownik=self.user,
            egzemplarz=self.egzemplarz
        )
        self.assertEqual(rezerwacja.uzytkownik, self.user)
        self.assertIsNotNone(rezerwacja.data_waznosci)

    def test_rezerwacja_zmiana_statusu(self):
        """Test czy widok rezerwacji zmienia status egzemplarza"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('rezerwuj_ksiazke', args=[self.egzemplarz.id]))
        
        self.egzemplarz.refresh_from_db()
        self.assertEqual(self.egzemplarz.status, 'zarezerwowany')
        self.assertEqual(response.status_code, 302)  # przekierowanie