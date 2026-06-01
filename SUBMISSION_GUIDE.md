# SUBMISSION_GUIDE

## Pliki do oddania

Oddaj cały katalog `BiblioTech` zawierający:

- `manage.py`
- `requirements.txt`
- `README.md`
- `PROJECT_OVERVIEW.md`
- `DIPLOMA_MAPPING.md`
- `config/` (z `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`)
- `books/` (z plikami `models.py`, `views.py`, `urls.py`, `admin.py`, `tests.py`, `forms.py`, `context_processors.py`, `migrations/`)
- `templates/`
- `static/` i `media/` jeśli w projekcie są używane obrazy lub pliki multimedialne wymagane do działania aplikacji

## Co nie musi być oddawane

Nie dołączaj do zestawu:

- `venv/`
- `db.sqlite3` (chyba że prowadzący konkretnie żąda bazy danych)
- `__pycache__/`
- `*.pyc`
- lokalne pliki archiwów `*.zip`

## Instrukcje uruchomienia

1. Utwórz i aktywuj środowisko wirtualne:

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

4. Utwórz użytkownika administracyjnego:

```powershell
venv\Scripts\python.exe manage.py createsuperuser
```

5. Uruchom serwer:

```powershell
venv\Scripts\python.exe manage.py runserver
```

6. Otwórz w przeglądarce:

- `http://127.0.0.1:8000/` — frontend aplikacji
- `http://127.0.0.1:8000/admin/` — panel administracyjny

## Jak sprawdzić działanie

- Uruchom testy:

```powershell
venv\Scripts\python.exe manage.py test books
```

- Jeżeli chcesz wygenerować dane testowe:

```powershell
venv\Scripts\python.exe manage.py seed_db
```

## Najważniejsze elementy do pokazania

- `README.md` — instrukcja uruchomienia i funkcje projektu.
- `PROJECT_OVERVIEW.md` — opis projektu, celów i technologii.
- `DIPLOMA_MAPPING.md` — mapowanie funkcjonalności do wymagań dyplomowych.
- `books/tests.py` — testy sprawdzające krytyczne scenariusze rezerwacji.

## Dodatkowe uwagi

- `config/settings.py` pracuje w trybie `DEBUG = True` dla środowiska deweloperskiego.
- `SECRET_KEY` jest zapisany w pliku dla lokalnego uruchomienia. W wersji produkcyjnej powinien być pobierany z zmiennej środowiskowej.
- `__debug__` jest włączone tylko w trybie developerskim i jest dostępne, jeśli zainstalowany jest `django-debug-toolbar`.
