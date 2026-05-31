# Katalog Books Grid - zmiany i lokalizacje

Ten plik opisuje, co zmieniłem w projekcie, aby:
- siatka książek była równa,
- każda karta była klikalna,
- przyciski wewnątrz karty działały niezależnie.

## Gdzie są zmiany

### 1. `BiblioTech/templates/katalog.html`
- główny widok katalogu książek.
- dodałem elementy:
  - `div.ksiazka-link` jako klikany kontener karty,
  - `data-href` do przechowywania linku do szczegółów książki,
  - skrypt JavaScript, który obsługuje kliknięcie i wciśnięcie klawisza Enter.
- usunąłem problem z zagnieżdżonymi linkami `<a>` w obrębie karty.
- filtr języka/ gatunku / liczby pozycji na stronę używa teraz klasy `filter-link` zamiast inline style.

### 2. `BiblioTech/books/static/css/style.css`
- główny styl strony.
- dodałem/zmodyfikowałem:
  - `.books-grid` z `display: grid` i `gap: 26px`, aby układ był równy,
  - `.ksiazka-link` jako blokowy kontener o pełnej wysokości,
  - `.ksiazka-content { display: flex; flex-direction: column; flex: 1; }`, aby zawartość karty rozciągała się i przyciski osadzane były u dołu,
  - `.filter-link` i `.filter-link.active` do wyświetlania aktywnych filtrów.

## Jak działa klikalna karta

- w `katalog.html` każdy element karty jest opakowany w `div.ksiazka-link`.
- wartość `data-href` zawiera link do szczegółów książki.
- skrypt JS w tym samym pliku:
  - przechwytuje kliknięcie na kartę,
  - ignoruje kliknięcie, gdy cel to przycisk `Wypożycz` lub `Zarezerwuj`,
  - przechodzi do strony książki w innych przypadkach.

## Dlaczego to było potrzebne

- poprzednio karta była opakowana w `<a>`, a wewnątrz były inne `<a>`, co powodowało niepoprawny HTML i problemy z zachowaniem.
- dzięki osobnemu kontenerowi `div` i skryptowi można mieć cały kafelek klikalny, a przyciski przy zachowaniu własnej funkcji.

## Co możesz sprawdzić

- `BiblioTech/templates/katalog.html` — logika widoku i obsługa kliknięć.
- `BiblioTech/books/static/css/style.css` — styl siatki i wyrównanie kart.
- w przeglądarce: czy przycisk `Wypożycz` działa bez przejścia do szczegółów książki, a kliknięcie w pustą część karty otwiera szczegóły.
