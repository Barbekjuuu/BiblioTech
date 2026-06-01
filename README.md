BiblioTech — krótkie instrukcje do demonstracji admina

Szybkie kroki do prezentacji funkcji rezerwacji przez pracownika biblioteki:

1. Uruchom serwer deweloperski:

```powershell
cd BiblioTech
venv\Scripts\activate
python manage.py runserver
```

2. Zaloguj się do panelu admina: `http://127.0.0.1:8000/admin/` (użyj konta superuser).

3. Przejdź do sekcji `Rezerwacje` (Books → Rezerwacje). Na stronie listy znajdziesz przycisk "Rezerwuj dla klienta".

4. Kliknij "Rezerwuj dla klienta" i wypełnij formularz:
   - wybierz konkretny egzemplarz (pole `Egzemplarz`),
   - wpisz adres e-mail klienta (jeśli konto nie istnieje, zostanie utworzone bez hasła),
   - opcjonalnie imię i nazwisko klienta.

5. Po utworzeniu rezerwacji egzemplarz otrzyma status `zarezerwowany`.

Uwagi:
- Admin ma akcję masową "Oznacz jako zwrócone" na liście rezerwacji.
- System waliduje, że wybrany egzemplarz jest dostępny.
- Jeśli chcesz wysyłać maile do użytkowników, skonfiguruj `EMAIL_*` w `config/settings.py`.
