# BiblioTech — Project Overview (dokumentacja do pracy dyplomowej)

## Cel projektu

BiblioTech to aplikacja biblioteczna napisana w Django, umożliwiająca przeglądanie katalogu, zarządzanie rezerwacjami i obsługę wypożyczeń. Projekt pokazuje projektowanie modelu domenowego, pracę z transakcjami bazodanowymi oraz rozszerzenie panelu administracyjnego.

## Szybki przegląd funkcji

- Rejestracja i logowanie użytkowników; profil z zakładkami `Wypożyczenia`, `Oczekujące`, `Powiadomienia`.
- Katalog z wyszukiwaniem, filtrem po gatunku i języku, paginacją i kartami książek.
- Strona szczegółów książki z informacją o dostępnych egzemplarzach.
- Sesyjny koszyk (wybór konkretnych egzemplarzy) oraz transakcyjne zatwierdzanie rezerwacji (zmiana statusu egzemplarza).
- System rezerwacji oczekujących z powiadomieniami (pole `powiadomiony` oraz model `Powiadomienie`).
- Panel admina z dodatkowymi akcjami: tworzenie rezerwacji dla klienta, walidacja dostępności egzemplarza, podgląd okładek.
- Komendy zarządzające (`seed_db`) do generowania danych testowych.
- Testy jednostkowe i integracyjne obejmujące krytyczne scenariusze rezerwacji i administrącji.

## Modele kluczowe

- `Autor`, `Gatunek`, `Ksiazka` — opis treści katalogu.
- `Egzemplarz` — egzemplarz fizyczny z polem statusu (dostępny/wypożyczony).
- `Rezerwacja` — powiązanie użytkownika z egzemplarzem, data utworzenia i (opcjonalnie) data zwrotu.
- `RezerwacjaOczekujaca` — wpis w kolejce oczekujących, z polem `powiadomiony`.
- `Powiadomienie` — obiekty powiadomień wysyłane do użytkowników.

## Zabezpieczenia i dobre praktyki

- Wszystkie operacje zmieniające stan (anuluj, zwrot, dodaj do koszyka, rezerwuj) używają metod POST i dekoratora `@require_POST`.
- Transakcje i blokady `select_for_update` przy zatwierdzaniu koszyka, aby uniknąć wyścigów i podwójnego przydziału egzemplarza.
- Migracje Django są up-to-date; testy uruchamiane na czystej bazie testowej przechodzą pomyślnie.

## Instrukcja uruchomienia (Windows)

1. Utwórz i aktywuj virtualenv (jeśli nie ma):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Zainstaluj zależności (jeśli potrzebne):

```powershell
pip install -r requirements.txt
```

3. Uruchom serwer developerski:

```powershell
cd BiblioTech
venv\Scripts\python.exe manage.py runserver
```

4. Uruchom testy:

```powershell
venv\Scripts\python.exe manage.py test books
```

## Mapowanie wymagań do pracy dyplomowej

- Cel funkcjonalny: separacja rezerwacji oczekujących od aktywnych wypożyczeń (`profile` z zakładkami) — dowód: [templates/profile.html](templates/profile.html#L1).
- Integralność danych: użycie transakcji i `select_for_update` przy zatwierdzaniu koszyka — dowód: `books/views.py` (`zatwierdz_koszyk`).
- Bezpieczeństwo: wszystkie mutujące endpointy oznaczone `@require_POST` oraz CSRF w formularzach — dowód: zmiany w `templates/katalog.html`, `templates/ksiazka_detail.html`, `templates/profile.html`.
- Obsługa administracyjna: możliwość rezerwacji egzemplarza dla klienta i tworzenia użytkownika z panelu admin — dowód: `books/admin.py` i `templates/admin/*`.
- Testy: pokrycie scenariuszy rezerwacji, oczekiwania i akcji administracyjnych — dowód: `books/tests.py` (16 testów, wszystkie przechodzą).

## Kolejne kroki (przygotowanie do obrony)

- Dodać krótkie slajdy/sekcję w README pokazującą scenariusz użytkownika i administratora.
- Opcjonalnie: implementacja wysyłki e-mail dla `Powiadomienie` (SMTP) — przydatne na prezentacji jako rozszerzenie.

---

Plik stworzony/aktualizowany jako część dokumentacji pracy dyplomowej.
