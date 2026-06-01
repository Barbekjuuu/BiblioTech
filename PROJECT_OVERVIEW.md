# BiblioTech - Project Overview

## Purpose

BiblioTech is a Django-based library system that allows users to browse books, filter by genre and language, add available copies to a reservation cart, and confirm reservations. The application is designed to be visually consistent with a dark/gold theme and provides a friendly user interface aligned with the home page styling.

## Key Features

- User registration, login, and profile management
- Catalog of books with search, filters, and pagination
- Book details page with availability status and borrowing actions
- Session-based cart for collecting selected book copies
- Reservation checkout that changes book copy status
- Admin panel with enhanced search, filters, and inline copy editing
- Seed command for generating test data using Faker
- Unit tests for models and reservation workflow

## Core Models

- `Autor` - author name and optional photo
- `Gatunek` - book genre
- `Ksiazka` - main book entity with title, description, cover, language, author, and genre
- `Egzemplarz` - physical copy of a book with availability status
- `Rezerwacja` - reservation connecting user and copy with expiration date

## Major Views

- `home` - home page with featured latest books and search bar
- `katalog` - catalog page with filters, pagination, and card-style navigation
- `ksiazka_detail` - detailed book view with cover, description, and availability
- `koszyk` - cart view with item list, remove button, and confirm reservation flow
- `profile` - user profile page with tabbed navigation for reservations and personal data

## Admin Support

- Custom admin for `Ksiazka` with `list_filter`, `search_fields`, and `EgzemplarzInline`
- Visual preview of covers and author photos in admin list
- Admin registration for all library models

## Technical Notes

- Uses Django sessions to track the cart before reservation confirmation
- Reservation expiration is automatically calculated as 14 days from creation
- `header-bg.png` is reused across pages for a consistent theme
- Templates include inline documentation comments for project defense

## How to Run

```bash
cd BiblioTech
venv\Scripts\python.exe manage.py runserver
```

To run tests:

```bash
venv\Scripts\python.exe manage.py test books
```

To seed data with Faker:

```bash
venv\Scripts\python.exe manage.py seed_db
```

## Defense Points

- Clear model relationships: one-to-many between books and copies, one-to-many between users and reservations
- Admin enhancements demonstrate Django admin customization
- Visual coherence across pages shows attention to UI/UX
- Test coverage proves basic workflow stability
- Session cart logic explains practical reservation staging
