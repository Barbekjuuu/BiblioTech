# BiblioTech

**BiblioTech** to system biblioteczny stworzony w Django, który umożliwia użytkownikom wypożyczanie książek, zgłaszanie oczekujących rezerwacji oraz zarządzanie tymi procesami przez panel administratora.

## Co zawiera projekt

- `books/` — aplikacja Django z logiką biznesową, modelami, widokami, adminem i testami.
- `config/` — konfiguracja projektu Django (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`).
- `templates/` — szablony HTML dla strony użytkownika.
- `static/` — pliki CSS i zasoby frontend.
- `media/` — miejsce na przesłane okładki i zdjęcia autorów.
- `requirements.txt` — lista bibliotek Python wymaganych do uruchomienia.
- `PROJECT_OVERVIEW.md` — opis projektu oraz celów pracy dyplomowej.
- `DIPLOMA_MAPPING.md` — mapowanie funkcji projektu do wymagań dyplomowych.
- `SUBMISSION_GUIDE.md` — instrukcja przygotowania pracy do oddania.

## Najważniejsze funkcje

### Użytkownik

- rejestracja i logowanie,
- przeglądanie katalogu książek z wyszukiwaniem i filtrem po gatunku oraz języku,
- strona szczegółów książki z opcją dodania do koszyka lub zgłoszenia rezerwacji oczekującej,
- sesyjny koszyk do wybierania konkretnych egzemplarzy,
- zatwierdzanie wypożyczeń i automatyczna zmiana statusu egzemplarzy,
- profil z zakładkami: `Wypożyczenia`, `Oczekujące`, `Powiadomienia`, `Dane osobowe`,
- anulowanie wypożyczeń i oczekujących rezerwacji oraz zwrot książki.

### Administrator

- panel admina Django z rozszerzeniami do wygodnego zarządzania,
- specjalny formularz `Rezerwuj dla klienta` do tworzenia rezerwacji konkretnego egzemplarza dla użytkownika,
- automatyczne tworzenie konta klienta po podaniu e-maila,
- walidacja dostępności egzemplarza przed utworzeniem rezerwacji,
- akcja masowa `Oznacz jako zwrócone` w panelu admina.

## Jak uruchomić projekt

1. Utwórz środowisko wirtualne i je aktywuj:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Zainstaluj wymagane pakiety:

```powershell
pip install -r requirements.txt
```

3. Utwórz i zastosuj migracje:

```powershell
venv\Scripts\python.exe manage.py makemigrations
venv\Scripts\python.exe manage.py migrate
```

4. Utwórz konto administratora:

```powershell
venv\Scripts\python.exe manage.py createsuperuser
```

5. Uruchom serwer Django:

```powershell
venv\Scripts\python.exe manage.py runserver
```

6. Otwórz przeglądarkę:

- `http://127.0.0.1:8000/` — interfejs użytkownika,
- `http://127.0.0.1:8000/admin/` — panel administratora.

## Testy

Uruchom wszystkie testy aplikacji `books`:

```powershell
venv\Scripts\python.exe manage.py test books
```

## Generowanie danych testowych

Aby wygenerować przykładowe dane testowe, użyj komendy:

```powershell
venv\Scripts\python.exe manage.py seed_db
```

## Struktura plików i co zmieniać

- `books/models.py` — modeluje książki, egzemplarze, rezerwacje i powiadomienia.
- `books/views.py` — realizuje logikę stron, akcje koszyka, rezerwacji i profilu.
- `books/urls.py` — definiuje ścieżki adresów URL dla aplikacji.
- `books/admin.py` — rozszerza panel administratora i dodaje dodatkowe akcje.
- `books/tests.py` — zawiera testy automatyczne weryfikujące działanie systemu.
- `templates/` — definiuje wygląd stron i przycisków.
- `config/settings.py` — ustawia parametry projektu, bazę danych i middleware.
- `config/urls.py` — łączy główne ścieżki URL i panel admina.

## Co jest już zrobione

- rezerwacje i wypożyczenia działają end-to-end,
- system kolejkowania oczekujących rezerwacji z powiadomieniami,
- wszystkie zmieniające stan akcje korzystają z formularzy POST i CSRF,
- transakcyjna obsługa koszyka przy zatwierdzaniu rezerwacji,
- dodatkowa funkcja admina: rezerwacja dla klienta,
- testy weryfikujące kluczowe scenariusze.

## Dodatkowe uwagi

- `DEBUG = True` w `config/settings.py` jest poprawne dla lokalnego środowiska.
- `SECRET_KEY` jest zapisany lokalnie; w produkcji powinien być przechowywany w zmiennej środowiskowej.
- Pliki `*.zip` zostały dodane do `.gitignore`, aby nie trafiały do repozytorium.
- Obecnie aplikacja używa powiadomień wewnętrznych; nie ma wbudowanej wysyłki e-mail.
