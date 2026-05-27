from django.core.management.base import BaseCommand
from books.models import Autor, Gatunek, Ksiazka, Egzemplarz
from faker import Faker
import random
import requests
from django.core.files.base import ContentFile

fake = Faker('pl_PL')

class Command(BaseCommand):
    help = 'Generuje testowe dane dla biblioteki'

    def handle(self, *args, **kwargs):
        self.stdout.write('Rozpoczynam generowanie danych...')

        # Gatunki
        gatunki_nazwy = ['Powieść', 'Fantastyka', 'Kryminał', 'Romans', 'Biografia', 'Historia', 'Science Fiction', 'Literatura młodzieżowa']
        gatunki = [Gatunek.objects.get_or_create(nazwa=nazwa)[0] for nazwa in gatunki_nazwy]

        # Autorzy
        for _ in range(15):
            Autor.objects.get_or_create(imie_nazwisko=fake.name())

        autorzy = Autor.objects.all()

        # Książki
        for _ in range(35):
            autor = random.choice(autorzy)
            gatunek = random.choice(gatunki)
            jezyk = random.choice(['pl', 'en', 'de', 'fr', 'es'])

            ksiazka = Ksiazka.objects.create(
                tytul=fake.sentence(nb_words=4).replace('.', ''),
                opis=fake.paragraph(nb_sentences=6),
                data_wydania=fake.date_between(start_date='-60y', end_date='today'),
                autor=autor,
                gatunek=gatunek,
                jezyk=jezyk
            )

            # Próba pobrania okładki
            try:
                response = requests.get(f'https://picsum.photos/id/{random.randint(100, 300)}/800/1200', timeout=8)
                if response.status_code == 200:
                    ksiazka.okladka.save(f'okladka_{ksiazka.id}.jpg', ContentFile(response.content), save=True)
            except:
                pass  # jeśli nie uda się pobrać - zostawiamy bez okładki

            # Egzemplarze
            for _ in range(random.randint(2, 6)):
                Egzemplarz.objects.create(
                    ksiazka=ksiazka,
                    status=random.choice(['dostepny', 'zarezerwowany'])
                )

        self.stdout.write(self.style.SUCCESS('Pomyślnie wygenerowano dane testowe!'))