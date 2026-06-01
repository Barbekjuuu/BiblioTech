# BiblioTech

BiblioTech to aplikacja biblioteczna napisana w Django 6.0.5. Umożliwia przeglądanie katalogu książek, dodawanie dostępnych egzemplarzy do koszyka, zatwierdzanie rezerwacji, zgłaszanie oczekujących rezerwacji oraz obsługę przez panel administracyjny.

## Zawartość projektu

- `books/` — aplikacja Django z modelami, widokami, URL-ami, adminem i testami.
- `config/` — konfiguracja projektu Django (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`).
- `templates/` — szablony HTML strony użytkownika i panelu admin.
- `media/` — miejsce na przesyłane okładki i zdjęcia autorów.
- `requirements.txt` — lista zależności Python.
- `PROJECT_OVERVIEW.md` — ogólny opis projektu i jego celów.
- `DIPLOMA_MAPPING.md` — mapowanie funkcjonalności projektu do wymagań pracy dyplomowej.

## Wymagania

Aplikacja wymaga Python 3.14 oraz pakietów z `requirements.txt`.

```powershell
pip install -r requirements.txt
```

## Uruchomienie lokalne

1. Utwórz środowisko wirtualne i je aktywuj:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Zainstaluj zależności:

```powershell
pip install -r requirements.txt
```

3. Utwórz migracje i zastosuj je:

```powershell
venv\Scripts\python.exe manage.py makemigrations
venv\Scripts\python.exe manage.py migrate
```

4. Utwórz superusera do panelu admina:

```powershell
venv\Scripts\python.exe manage.py createsuperuser
```

5. Uruchom serwer:

```powershell
venv\Scripts\python.exe manage.py runserver
```

6. Wejdź do aplikacji:

- Frontend: `http://127.0.0.1:8000/`
- Panel admin: `http://127.0.0.1:8000/admin/`

## Funkcje użytkownika

- Rejestracja i logowanie.
- Przeglądanie katalogu książek z filtrem po gatunku, języku i wyszukiwaniem.
- Dodawanie dostępnych egzemplarzy do koszyka oraz zatwierdzanie wypożyczeń.
- Zgłaszanie oczekujących rezerwacji dla książek, które nie są dostępne.
- Profil z zakładkami: `Wypożyczenia`, `Oczekujące`, `Powiadomienia`, `Dane osobowe`.
- Anulowanie rezerwacji i zwroty.

## Funkcje administracyjne

- Szybkie filtrowanie, wyszukiwanie i podgląd danych w panelu admin.
- Dodatkowy formularz "Rezerwuj dla klienta" w adminie do rezerwacji konkretnego egzemplarza dla użytkownika.
- Walidacja dostępności egzemplarza przy rezerwacji przez admina.
- Akcja masowa `Oznacz jako zwrócone` dla rezerwacji.

## Testy

Uruchom testy jednostkowe:

```powershell
venv\Scripts\python.exe manage.py test books
```

## Dokumentacja projektu

- `PROJECT_OVERVIEW.md` — opis projektu i celów.
- `DIPLOMA_MAPPING.md` — objaśnienie spełnionych wymagań pracy dyplomowej.

## Uwagi bezpieczeństwa

- W trybie developerskim `DEBUG = True` w `config/settings.py`.
- `SECRET_KEY` jest zdefiniowany w kodzie dla lokalnego uruchomienia; w środowisku produkcyjnym powinien być przechowywany w zmiennych środowiskowych.

## Dodatkowe uwagi

- `db.sqlite3` oraz katalog `media/` są ignorowane w `.gitignore`.
- Jeśli chcesz używać wysyłki e-mail, skonfiguruj odpowiednie ustawienia `EMAIL_*` w `config/settings.py`.
- Archiwów ZIP generowanych lokalnie nie ma sensu dodawać do repozytorium; są ignorowane przy dodaniu `*.zip` do `.gitignore`.
