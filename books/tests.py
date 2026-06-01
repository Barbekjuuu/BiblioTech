from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Autor, Gatunek, Ksiazka, Egzemplarz, Rezerwacja, RezerwacjaOczekujaca, Powiadomienie
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

    def test_confirm_cart_fails_if_book_unavailable(self):
        """Testuje, że zatwierdzenie koszyka kończy się błędem, gdy książka przestanie być dostępna."""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('dodaj_do_koszyka', args=[self.egzemplarz.id]))
        self.assertEqual(response.status_code, 302)

        self.egzemplarz.status = 'zarezerwowany'
        self.egzemplarz.save()

        response = self.client.post(reverse('zatwierdz_koszyk'))
        self.assertRedirects(response, reverse('koszyk'))
        self.assertEqual(Rezerwacja.objects.count(), 0)

    def test_cancel_waiting_reservation(self):
        """Testuje anulowanie oczekującej rezerwacji."""
        self.egzemplarz.status = 'zarezerwowany'
        self.egzemplarz.save()

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('zarezerwuj_ksiazke', args=[self.ksiazka.id]))
        self.assertRedirects(response, reverse('ksiazka_detail', args=[self.ksiazka.id]))

        oczekujaca = RezerwacjaOczekujaca.objects.get(uzytkownik=self.user, ksiazka=self.ksiazka)
        response = self.client.post(reverse('anuluj_rezerwacje_oczekujaca', args=[oczekujaca.id]))
        self.assertRedirects(response, reverse('profile') + '?tab=oczekujace')
        oczekujaca.refresh_from_db()
        self.assertFalse(oczekujaca.aktywna)

    def test_waiting_request_deactivates_when_checkout(self):
        """Testuje dezaktywację oczekującego zgłoszenia po zatwierdzeniu rezerwacji."""
        self.egzemplarz.status = 'zarezerwowany'
        self.egzemplarz.save()

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('zarezerwuj_ksiazke', args=[self.ksiazka.id]))
        self.assertRedirects(response, reverse('ksiazka_detail', args=[self.ksiazka.id]))

        oczekujaca = RezerwacjaOczekujaca.objects.get(uzytkownik=self.user, ksiazka=self.ksiazka)
        self.assertTrue(oczekujaca.aktywna)

        self.egzemplarz.status = 'dostepny'
        self.egzemplarz.save()
        response = self.client.post(reverse('dodaj_do_koszyka', args=[self.egzemplarz.id]))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('zatwierdz_koszyk'))
        self.assertEqual(response.status_code, 302)

        oczekujaca.refresh_from_db()
        self.assertFalse(oczekujaca.aktywna)

    def test_return_reservation_makes_copy_available(self):
        """Testuje zwrot rezerwacji i przywrócenie egzemplarza do dostępnych."""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('dodaj_do_koszyka', args=[self.egzemplarz.id]))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('zatwierdz_koszyk'))
        self.assertEqual(response.status_code, 302)

        rezerwacja = Rezerwacja.objects.first()
        response = self.client.post(reverse('zwroc_rezerwacje', args=[rezerwacja.id]))

        self.assertRedirects(response, reverse('profile') + '?tab=wypozyczenia')
        rezerwacja.refresh_from_db()
        self.egzemplarz.refresh_from_db()
        self.assertIsNotNone(rezerwacja.data_zwrotu)
        self.assertEqual(self.egzemplarz.status, 'dostepny')

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

    def test_waiting_reservation_request(self):
        """Test zgłoszenia oczekującej rezerwacji dla niedostępnej książki."""
        self.egzemplarz.status = 'zarezerwowany'
        self.egzemplarz.save()

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('zarezerwuj_ksiazke', args=[self.ksiazka.id]))

        self.assertRedirects(response, reverse('ksiazka_detail', args=[self.ksiazka.id]))
        oczekujaca = RezerwacjaOczekujaca.objects.filter(uzytkownik=self.user, ksiazka=self.ksiazka, aktywna=True)
        self.assertEqual(oczekujaca.count(), 1)

    def test_cancel_reservation_redirects_to_wypozyczenia(self):
        """Testuje anulowanie wypożyczenia i powrót do zakładki wypożyczenia."""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('dodaj_do_koszyka', args=[self.egzemplarz.id]))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('zatwierdz_koszyk'))
        self.assertEqual(response.status_code, 302)

        rezerwacja = Rezerwacja.objects.first()
        response = self.client.post(reverse('anuluj_rezerwacje', args=[rezerwacja.id]))

        self.assertRedirects(response, reverse('profile') + '?tab=wypozyczenia')
        self.assertFalse(Rezerwacja.objects.filter(id=rezerwacja.id).exists())

    def test_waiting_reservation_not_created_when_book_available(self):
        """Test, że rezerwacja oczekująca nie jest tworzona, gdy książka jest dostępna."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('zarezerwuj_ksiazke', args=[self.ksiazka.id]))

        self.assertRedirects(response, reverse('ksiazka_detail', args=[self.ksiazka.id]))
        self.assertFalse(RezerwacjaOczekujaca.objects.filter(uzytkownik=self.user, ksiazka=self.ksiazka).exists())

    def test_mark_all_notifications_read(self):
        """Test zbiorczego oznaczania powiadomień jako przeczytanych."""
        Powiadomienie.objects.create(
            uzytkownik=self.user,
            tytul='Dostępna książka',
            tresc='Książka jest teraz dostępna.',
        )
        Powiadomienie.objects.create(
            uzytkownik=self.user,
            tytul='Przypomnienie',
            tresc='Masz nowe powiadomienie.',
        )

        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('oznacz_wszystkie_powiadomienia_przeczytane'))

        self.assertRedirects(response, reverse('profile') + '?tab=powiadomienia')
        self.assertEqual(self.user.powiadomienia.filter(przeczytane=False).count(), 0)

    def test_admin_create_reservation_for_user(self):
        """Testuje, że pracownik admin może utworzyć rezerwację dla klienta."""
        # utwórz superusera i zaloguj się
        admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
        self.client.force_login(admin)

        url = reverse('admin:books_rezerwacja_create_for_user')
        data = {
            'egzemplarz': str(self.egzemplarz.id),
            'email': 'nowyklient@example.com',
            'first_name': 'Anna',
            'last_name': 'Nowak'
        }

        response = self.client.post(url, data)
        # should redirect to rezerwacja changelist
        self.assertEqual(response.status_code, 302)
        # reservation created
        self.assertTrue(Rezerwacja.objects.filter(egzemplarz=self.egzemplarz).exists())
        self.egzemplarz.refresh_from_db()
        self.assertEqual(self.egzemplarz.status, 'zarezerwowany')

    def test_admin_create_reservation_fails_if_copy_unavailable(self):
        """Walidacja: admin nie może rezerwować egzemplarza, który nie jest dostępny."""
        admin = User.objects.create_superuser(username='admin2', email='admin2@example.com', password='adminpass')
        self.client.force_login(admin)

        # ustaw egzemplarz jako zarezerwowany
        self.egzemplarz.status = 'zarezerwowany'
        self.egzemplarz.save()

        url = reverse('admin:books_rezerwacja_create_for_user')
        data = {
            'egzemplarz': str(self.egzemplarz.id),
            'email': 'klient2@example.com',
        }

        response = self.client.post(url, data)
        # form should be re-rendered with error
        self.assertEqual(response.status_code, 200)
        self.assertIn('Wybrany egzemplarz nie jest dostępny do rezerwacji.', response.content.decode('utf-8'))
