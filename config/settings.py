"""
Django settings for BiblioTech project.

Projekt dyplomowy: System zarządzania biblioteką
"""

from pathlib import Path

# Ścieżka bazowa projektu
BASE_DIR = Path(__file__).resolve().parent.parent

# Klucz bezpieczeństwa projektu (nie udostępniać publicznie)
SECRET_KEY = 'django-insecure-p0c2srv(b^$=5)m)!h4x^akco675j9gvd%a11=o2k+zjs&v@8k'

# Tryb developerski - w produkcji należy ustawić na False
DEBUG = True

ALLOWED_HOSTS = []

# ====================== ZAINSTALOWANE APLIKACJE ======================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'books',                    # Aplikacja biblioteczna - dodanie aplikacja biblioteczna
    
    # Narzędzie do debugowania podczas developmentu
    'debug_toolbar',
]

# ====================== MIDDLEWARE ======================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Debug Toolbar Middleware
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # Globalny folder na szablony HTML
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ====================== BAZA DANYCH ======================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ====================== WALIDACJA HASEŁ ======================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ====================== USTAWIENIA MIĘDZYNARODOWE ======================
LANGUAGE_CODE = 'pl'                    # Język interfejsu - polski
TIME_ZONE = 'Europe/Warsaw'             # Strefa czasowa Polski

USE_I18N = True                         # Włączenie internacjonalizacji
USE_TZ = True                           # Używanie stref czasowych

# ====================== PLIKI STATYCZNE I MEDIA ======================
STATIC_URL = 'static/'                  # URL do plików statycznych (CSS, JS)
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Folder do zbierania plików statycznych

MEDIA_URL = 'media/'                    # URL do przesyłanych plików (zdjęcia)
MEDIA_ROOT = BASE_DIR / 'media'         # Folder, w którym będą zapisywane zdjęcia okładek i autorów

# ====================== DEBUG TOOLBAR ======================
INTERNAL_IPS = [
    '127.0.0.1',
]