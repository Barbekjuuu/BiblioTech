# BiblioTech — prezentacja dla laika

## Co to jest BiblioTech?

BiblioTech to aplikacja biblioteczna, która pozwala wypożyczać książki online i rezerwować je, gdy nie są dostępne. To proste narzędzie, które symuluje pracę biblioteki: użytkownik może przeglądać katalog, wybierać książki i zarządzać swoimi wypożyczeniami.

## Co mogą robić użytkownicy?

1. Zarejestrować się i zalogować.
2. Przejść do katalogu książek.
3. Filtrować książki po gatunku i języku, szukać po tytule.
4. Na stronie książki zobaczyć, czy egzemplarz jest dostępny.
5. Dodać dostępny egzemplarz do koszyka.
6. Zatwierdzić wypożyczenie w koszyku.
7. W profilu zobaczyć aktywne wypożyczenia, oczekujące rezerwacje i powiadomienia.
8. Anulować wypożyczenia lub oczekujące rezerwacje.
9. Zwrócić książkę i automatycznie przywrócić ją do dostępnych egzemplarzy.

## Co widzi administrator?

Administrator w panelu `Django admin` może:

- przeglądać książki, egzemplarze i rezerwacje,
- tworzyć rezerwacje dla klienta, nawet jeśli klient jeszcze nie ma konta,
- oznaczać rezerwacje jako zwrócone masowo.

## Jak działa BiblioTech — w prostych słowach

- W aplikacji jest katalog książek.
- Każda książka ma konkretne egzemplarze.
- Jeżeli egzemplarz jest dostępny, użytkownik może go wypożyczyć.
- Jeśli nie ma dostępnych egzemplarzy, użytkownik może zgłosić oczekującą rezerwację.
- Gdy egzemplarz zostaje zwrócony, pierwsza osoba z oczekujących dostaje powiadomienie.

## Czemu to jest dobre?

- Dzieli realną bibliotekę na dwa stany: dostępne wypożyczenia i zgłoszone oczekiwania.
- Umożliwia pracownikowi obsługę klienta przez panel administracyjny.
- Pokazuje, jak działa logiczne przechowywanie danych, bez konieczności wiedzy programistycznej.

## Co warto pokazać na obronie?

1. Strona główna i katalog książek.
2. Strona szczegółów książki:
   - dostępne egzemplarze,
   - przycisk „Wypożycz” lub „Zarezerwuj”.
3. Koszyk z wybranymi egzemplarzami.
4. Zatwierdzenie wypożyczenia i przejście do profilu.
5. Zakładka `Wypożyczenia` w profilu.
6. Zakładka `Oczekujące` w profilu.
7. Zakładka `Powiadomienia` w profilu.
8. Panel admina:
   - lista rezerwacji,
   - przycisk `Rezerwuj dla klienta`,
   - tworzenie rezerwacji dla klienta.

## Jak się uczyć z tej prezentacji?

- Nie musisz znać Pythona, aby zrozumieć działanie aplikacji.
- Myśl o niej jak o sklepie internetowym, tylko zamiast kupowania książek, je wypożyczasz.
- Jeżeli chcesz wiedzieć, gdzie edytować wygląd strony — sprawdź folder `templates/`.
- Jeżeli chcesz wiedzieć, gdzie zmieniać zasady biznesowe — sprawdź `books/views.py`.
- Jeżeli chcesz wiedzieć, gdzie zmieniać dane w bazie — sprawdź `books/models.py`.

## Gdzie co jest ważne?

- `books/models.py` — tutaj są zapisane zasady procesu: dostępność, rezerwacje, oczekiwanie.
- `books/views.py` — tutaj jest logika, kto co może zrobić.
- `books/urls.py` — tutaj są adresy, które łączą strony.
- `books/admin.py` — tutaj jest rozszerzony panel dla pracownika biblioteki.
- `templates/` — to wygląd strony i przyciski.

## Krótkie przykłady

- `Dodaj do koszyka` — użytkownik wybiera konkretny egzemplarz i przechowuje go w sesji.
- `Zatwierdź koszyk` — aplikacja tworzy rezerwację i blokuje egzemplarz.
- `Zarezerwuj` — jeżeli książka nie jest dostępna, użytkownik zgłasza oczekującą rezerwację.
- `Powiadomienie` — użytkownik dostaje informację, gdy egzemplarz wraca do biblioteki.

## Gotowe zdania do obrony

- "BiblioTech to system biblioteczny z obsługą koszyka oraz listy oczekujących."
- "Użytkownik widzi osobno aktywne wypożyczenia i zgłoszone oczekiwania."
- "Administrator może zarezerwować konkretny egzemplarz dla klienta w panelu admina."
- "System używa Django i wykorzystuje testy automatyczne, żeby sprawdzić najważniejsze scenariusze."
