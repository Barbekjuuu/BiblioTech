from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Autor, Gatunek, Ksiazka, Egzemplarz, Rezerwacja
from django.urls import reverse
from django.utils import timezone


class BiblioTechTests(TestCase):
    """Zestaw testów podstawowych funkcji aplikacji BiblioTech."""

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
        """Test modelu Książka."""
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
        """Test czy dodanie do koszyka i zatwierdzenie zmienia status egzemplarza."""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('dodaj_do_koszyka', args=[self.egzemplarz.id]))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('zatwierdz_koszyk'))
        self.assertEqual(response.status_code, 302)

        self.egzemplarz.refresh_from_db()
        self.assertEqual(self.egzemplarz.status, 'zarezerwowany')

    def test_profile_update(self):
        """Test aktualizacji danych osobowych użytkownika."""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(
            reverse('profile') + '?tab=dane',
            {
                'form_type': 'profile',
                'email': 'nowy@example.com',
                'first_name': 'Jan',
                'last_name': 'Nowak',
            }
        )

        self.assertRedirects(response, reverse('profile') + '?tab=dane')
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'nowy@example.com')
        self.assertEqual(self.user.first_name, 'Jan')
        self.assertEqual(self.user.last_name, 'Nowak')

    def test_password_change(self):
        """Test zmiany hasła przez użytkownika."""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(
            reverse('profile') + '?tab=haslo',
            {
                'form_type': 'password',
                'old_password': 'testpass123',
                'new_password1': 'newpass456',
                'new_password2': 'newpass456',
            }
        )

        self.assertRedirects(response, reverse('profile') + '?tab=haslo')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass456'))
