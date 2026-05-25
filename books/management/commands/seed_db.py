from django.core.management.base import BaseCommand
from faker import Faker
from books.models import Autor, Gatunek, Ksiazka, Egzemplarz
import random

fake = Faker('pl_PL')

class Command(BaseCommand):
    help = 'Generuje testowe dane do biblioteki'

    def handle(self, *args, **options):
        self.stdout.write('Rozpoczynam generowanie danych...')

        # Tworzymy gatunki
        gatunki = ['Fantastyka', 'Kryminał', 'Romans', 'Thriller', 'Horror', 'Biografia', 'Historia', 'Nauka', 'Literatura faktu']
        for nazwa in gatunki:
            Gatunek.objects.get_or_create(nazwa=nazwa)

        # Tworzymy autorów
        for _ in range(15):
            autor = Autor.objects.create(
                imie_nazwisko=fake.name()
            )

        # Tworzymy książki
        for _ in range(30):
            autor = random.choice(Autor.objects.all())
            gatunek = random.choice(Gatunek.objects.all())
            
            ksiazka = Ksiazka.objects.create(
                tytul=fake.sentence(nb_words=6)[:-1],
                opis=fake.paragraph(nb_sentences=5),
                data_wydania=fake.date_between(start_date='-30y', end_date='today'),
                autor=autor,
                gatunek=gatunek,
            )

            # Tworzymy 2-5 egzemplarzy każdej książki
            for _ in range(random.randint(2, 5)):
                Egzemplarz.objects.create(
                    ksiazka=ksiazka,
                    status=random.choice(['dostepny', 'wypozyczony', 'zarezerwowany'])
                )

        self.stdout.write(self.style.SUCCESS('Pomyślnie wygenerowano dane testowe!'))