import environ
from pathlib import Path
import dj_database_url
import os
if os.environ.get("RAILWAY_ENVIRONMENT"):
    # siamo in Railway: NON leggere il file .env
    env = environ.Env(DEBUG=(bool, False))
else:
    # siamo in locale: carica .env
    env = environ.Env(DEBUG=(bool, False))
    env.read_env()


# 1) Legge il .env nella root
env = environ.Env(
    # casting e valori di default
    DEBUG=(bool, False),
)
env.read_env()   # carica le variabili da .env

# 2) Base dir
BASE_DIR = Path(__file__).resolve().parent.parent

# 3) Sicurezza
SECRET_KEY = env('DJANGO_SECRET_KEY')  # dal .env
DEBUG      = env('DEBUG')              # dal .env
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])

# 4) Installed apps, middleware, etc...
INSTALLED_APPS = [
    'django.contrib.admin',
    # ...
    'accounts',
    'music',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ...
]

ROOT_URLCONF = 'music_streaming.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':    [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': { 'context_processors': [
            'django.template.context_processors.debug',
            # ...
        ]},
    },
]
WSGI_APPLICATION = 'music_streaming.wsgi.application'
ASGI_APPLICATION = 'music_streaming.asgi.application'

# 5) Database

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=not DEBUG
    )
}

# 6) Validators, Internationalization, Static, ecc.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # ...
]
LANGUAGE_CODE = 'it-it'
TIME_ZONE     = 'Europe/Rome'
USE_I18N      = True
USE_TZ        = True

STATIC_URL        = '/static/'
STATICFILES_DIRS  = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL     = 'accounts.User'
LOGIN_URL           = 'accounts:login'
LOGIN_REDIRECT_URL  = 'music:song-list'
LOGOUT_REDIRECT_URL = 'accounts:login'
