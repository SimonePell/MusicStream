from pathlib import Path
import os

# 1) Base directory del progetto
BASE_DIR = Path(__file__).resolve().parent.parent

# 2) Sicurezza
SECRET_KEY = 'django-insecure-[LA_TUA_SECRET_KEY_QUI]'
DEBUG = True
ALLOWED_HOSTS = []  # In produzione inserisci i tuoi host/domain

# 3) Applicazioni installate
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Le tue app
    'accounts',    # autenticazione, profili e gruppi
    'music',       # canzoni, generi, playlist, raccomandazioni
]

# 4) Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 5) URL dispatcher
ROOT_URLCONF = 'music_streaming.urls'

# 6) Template engine + Bootstrap static
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # cartella per template globali
        'APP_DIRS': True,                  # cerca template in ogni app sotto templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 7) WSGI e ASGI entrypoints
WSGI_APPLICATION = 'music_streaming.wsgi.application'
ASGI_APPLICATION = 'music_streaming.asgi.application'

# 8) Database: PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'musicdb',
        'USER': 'musicuser',
        'PASSWORD': '1TierPol9!',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 9) Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 10) Internazionalizzazione
LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_TZ = True

# 11) Static files (CSS, JS, immagini)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']       # sviluppo
# STATIC_ROOT = BASE_DIR / 'staticfiles'       # in produzione con collectstatic

# 12) Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 13) Modello User personalizzato
AUTH_USER_MODEL = 'accounts.User'

# 14) URL login/logout di comodo
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'music:song-list'
LOGOUT_REDIRECT_URL = 'accounts:login'
