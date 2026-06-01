# Mapowanie funkcji projektu do wymagań pracy dyplomowej

Poniżej znajduje się krótkie, dowodowe mapowanie implementowanych funkcji na kryteria oceniane w pracy dyplomowej.

## 1. Separacja rezerwacji oczekujących i aktywnych wypożyczeń
- Cel: użytkownik widzi oddzielnie swoje aktywne wypożyczenia i zgłoszenia oczekujące.
- Dowód: szablon i logika profilu z zakładkami — [templates/profile.html](templates/profile.html)

Przykładowy fragment widoku `profile` (logika wyboru zakładki i przygotowanie kontekstu):

```python
def profile(request):
  tab = request.GET.get('tab', 'rezerwacje')
  rezerwacje = request.user.rezerwacje.filter(data_zwrotu__isnull=True).order_by('-data_rezerwacji')
  rezerwacje_oczekujace = request.user.oczekujace_rezerwacje.filter(aktywna=True).order_by('-data_zgloszenia')
  kontekst = { 'rezerwacje': rezerwacje, 'rezerwacje_oczekujace': rezerwacje_oczekujace, 'active_tab': tab }
  return render(request, 'profile.html', kontekst)
```

## 2. Integralność danych i obsługa współbieżności
- Cel: zapobiec podwójnemu przydziałowi tego samego egzemplarza w konkurencyjnych operacjach.
- Dowód: użycie transakcji i `select_for_update` w procesie zatwierdzania koszyka — [books/views.py](books/views.py)

Fragment transakcyjnego zatwierdzania koszyka (`zatwierdz_koszyk`) pokazujący `transaction.atomic` i `select_for_update`:

```python
def zatwierdz_koszyk(request):
  koszyk_ids = request.session.get('koszyk', [])
  try:
    with transaction.atomic():
      for egz_id in koszyk_ids:
        egzemplarz = get_object_or_404(
          Egzemplarz.objects.select_for_update(),
          id=egz_id,
          status='dostepny'
        )
        rezerwacja = Rezerwacja.objects.create(uzytkownik=request.user, egzemplarz=egzemplarz)
        egzemplarz.status = 'zarezerwowany'
        egzemplarz.save()
  except Http404:
    messages.error(request, 'One or more books in your cart are no longer available.')
    return redirect('koszyk')
```

## 3. Bezpieczeństwo operacji mutujących stan
- Cel: wszystkie zmiany stanu wykonują się przez POST oraz chronione są CSRF.
- Dowód: dekoratory `@require_POST` i formularze z `{% csrf_token %}` w szablonach:
  - [books/views.py](books/views.py)
  - [templates/katalog.html](templates/katalog.html)
  - [templates/ksiazka_detail.html](templates/ksiazka_detail.html)
  - [templates/profile.html](templates/profile.html)

Przykład dekoratora i formularza (widok + fragment szablonu):

```python
@login_required
@require_POST
def zarezerwuj_ksiazke(request, ksiazka_id):
    ksiazka = get_object_or_404(Ksiazka, id=ksiazka_id)
    ...
```

```html
<form action="{% url 'zarezerwuj_ksiazke' ksiazka.id %}" method="post">
  {% csrf_token %}
  <button type="submit">Zarezerwuj</button>
</form>
```

## 4. Funkcje administracyjne i walidacja
- Cel: bibliotekarz może zarezerwować konkretny egzemplarz dla klienta, z walidacją dostępności.
- Dowód: rozszerzenia admina i formularz rezerwacji dla klienta — [books/admin.py](books/admin.py) oraz szablony w [templates/admin/](templates/admin/)

Fragment z `books/admin.py` pokazujący walidację i tworzenie rezerwacji dla klienta z panelu admin:

```python
def create_for_user_view(self, request):
  if request.method == 'POST':
    form = self.ReserveForUserForm(request.POST)
    if form.is_valid():
      egz = form.cleaned_data['egzemplarz']
      if egz.status != 'dostepny':
        form.add_error('egzemplarz', 'Wybrany egzemplarz nie jest dostępny do rezerwacji.')
      else:
        user, created = User.objects.get_or_create(email=email, defaults={'username': username})
        rezerwacja = Rezerwacja.objects.create(uzytkownik=user, egzemplarz=egz)
        egz.status = 'zarezerwowany'
        egz.save()
```

## 5. Testy i demonstracja poprawności działania
- Cel: pokazać scenariusze krytyczne (rezerwacja, anulowanie, powiadomienia) automatycznymi testami.
- Dowód: testy jednostkowe i integracyjne obejmujące 16 przypadków — [books/tests.py](books/tests.py)

Przykłady testów (fragmenty z `books/tests.py`):

```python
def test_rezerwacja_zmiana_statusu(self):
  self.client.login(username='testuser', password='testpass123')
  response = self.client.post(reverse('dodaj_do_koszyka', args=[self.egzemplarz.id]))
  response = self.client.post(reverse('zatwierdz_koszyk'))
  self.egzemplarz.refresh_from_db()
  self.assertEqual(self.egzemplarz.status, 'zarezerwowany')
```

```python
def test_admin_create_reservation_for_user(self):
  admin = User.objects.create_superuser(...)
  self.client.force_login(admin)
  response = self.client.post(reverse('admin:books_rezerwacja_create_for_user'), data)
  self.assertTrue(Rezerwacja.objects.filter(egzemplarz=self.egzemplarz).exists())
```

## 6. Przygotowanie do prezentacji i rozszerzenia
- Zalecane dodatkowe elementy do demonstracji:
  - Krótkie slajdy z przepływem użytkownika i administratora (screenshots szablonów).
  - Opcjonalna wysyłka e-mail dla `Powiadomienie` (implementacja SMTP) jako punkt rozbudowy.

---

Plik wygenerowany automatycznie jako pomoc w przygotowaniu obrony. Jeśli chcesz, rozbuduję każdą pozycję o konkretne fragmenty kodu (fragmenty / linie) oraz polecenia do uruchomienia demonstracji.