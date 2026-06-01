# Mapowanie funkcji projektu do wymagań pracy dyplomowej

Poniżej znajduje się krótkie, dowodowe mapowanie implementowanych funkcji na kryteria oceniane w pracy dyplomowej.

## 1. Separacja rezerwacji oczekujących i aktywnych wypożyczeń
- Cel: użytkownik widzi oddzielnie swoje aktywne wypożyczenia i zgłoszenia oczekujące.
- Dowód: szablon i logika profilu z zakładkami — [templates/profile.html](templates/profile.html)

## 2. Integralność danych i obsługa współbieżności
- Cel: zapobiec podwójnemu przydziałowi tego samego egzemplarza w konkurencyjnych operacjach.
- Dowód: użycie transakcji i `select_for_update` w procesie zatwierdzania koszyka — [books/views.py](books/views.py)

## 3. Bezpieczeństwo operacji mutujących stan
- Cel: wszystkie zmiany stanu wykonują się przez POST oraz chronione są CSRF.
- Dowód: dekoratory `@require_POST` i formularze z `{% csrf_token %}` w szablonach:
  - [books/views.py](books/views.py)
  - [templates/katalog.html](templates/katalog.html)
  - [templates/ksiazka_detail.html](templates/ksiazka_detail.html)
  - [templates/profile.html](templates/profile.html)

## 4. Funkcje administracyjne i walidacja
- Cel: bibliotekarz może zarezerwować konkretny egzemplarz dla klienta, z walidacją dostępności.
- Dowód: rozszerzenia admina i formularz rezerwacji dla klienta — [books/admin.py](books/admin.py) oraz szablony w [templates/admin/](templates/admin/)

## 5. Testy i demonstracja poprawności działania
- Cel: pokazać scenariusze krytyczne (rezerwacja, anulowanie, powiadomienia) automatycznymi testami.
- Dowód: testy jednostkowe i integracyjne obejmujące 16 przypadków — [books/tests.py](books/tests.py)

## 6. Przygotowanie do prezentacji i rozszerzenia
- Zalecane dodatkowe elementy do demonstracji:
  - Krótkie slajdy z przepływem użytkownika i administratora (screenshots szablonów).
  - Opcjonalna wysyłka e-mail dla `Powiadomienie` (implementacja SMTP) jako punkt rozbudowy.

---

Plik wygenerowany automatycznie jako pomoc w przygotowaniu obrony. Jeśli chcesz, rozbuduję każdą pozycję o konkretne fragmenty kodu (fragmenty / linie) oraz polecenia do uruchomienia demonstracji.