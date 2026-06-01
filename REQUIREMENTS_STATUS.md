# REQUIREMENTS_STATUS

## Sprawdzenie wymagań projektu BiblioTech

### Zaimplementowane elementy

- [x] Struktura projektu Django (`manage.py`, `config/`, `books/`).
- [x] Uwierzytelnianie użytkowników (rejestracja, logowanie).
- [x] Katalog książek z wyszukiwaniem i filtrowaniem.
- [x] Strona szczegółów książki z informacją o dostępności.
- [x] Sesyjny koszyk dla konkretnych egzemplarzy.
- [x] Zatwierdzanie wypożyczeń i zmiana statusu egzemplarza.
- [x] Rezerwacje oczekujące przy braku dostępnych egzemplarzy.
- [x] Profil użytkownika z zakładkami dla wypożyczeń, oczekujących rezerwacji i powiadomień.
- [x] Anulowanie rezerwacji, zwroty i dezaktywacja oczekujących rezerwacji.
- [x] Powiadomienia wewnętrzne dla użytkownika.
- [x] Niestandardowe rozszerzenia admina (rezerwacja dla klienta, walidacja, akcja masowa zwrotu).
- [x] Zabezpieczenie mutujących operacji przez `POST` i CSRF.
- [x] Testy automatyczne obejmujące scenariusze rezerwacji, oczekiwania i admina.
- [x] Dokumentacja projektu w `README.md`, `PROJECT_OVERVIEW.md`, `DIPLOMA_MAPPING.md`, `SUBMISSION_GUIDE.md`.

### Elementy wymagające uwagi / opcjonalne

- [ ] Wysyłka e-mail powiadomień nie jest zaimplementowana; obecnie powiadomienia działają w aplikacji.
- [ ] W `config/settings.py` `DEBUG = True`, co jest dopuszczalne dla lokalnej wersji, ale w produkcji powinno być ustawione na `False`.
- [ ] `SECRET_KEY` jest zapisany w pliku. Dla produkcji lepiej użyć zmiennej środowiskowej.
- [ ] `db.sqlite3` jest obecny lokalnie; w repo powinna zostać wydzielona informacja, czy zostawić bazę, czy ją wygenerować.

### Stan projektu

- [x] `python manage.py check` — brak problemów.
- [x] `python manage.py test books` — wszystkie testy przeszły.

### Zalecenia do oddania

- Oddaj katalog `BiblioTech/` bez `venv/`, bez `db.sqlite3` (chyba że prowadzący wymaga), bez `*.zip`.
- Dołącz dokumenty:
  - `README.md`,
  - `SUBMISSION_GUIDE.md`,
  - `PROJECT_OVERVIEW.md`,
  - `DIPLOMA_MAPPING.md`,
  - `REQUIREMENTS_STATUS.md`.
