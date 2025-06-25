import os
from pathlib import Path

import dj_database_url
import environ

# 1) Base dir
BASE_DIR = Path(__file__).resolve().parent.parent

# 2) Carica il .env solo in locale (Railway non avrà un file .env)
if not os.environ.get("RAILWAY_ENVIRONMENT"):
    environ.Env.read_env()

# 3) Env con casting e default
env = environ.Env(
    DEBUG=(bool, False),
)

# 4) Sicurezza
SECRET_KEY     = env("DJANGO_SECRET_KEY")
DEBUG          = env("DEBUG")
ALLOWED_HOSTS  = env.list("DJANGO_ALLOWED_HOSTS", default=[])

# 5) Installed apps, middleware, ecc.
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
WSGI_APPLICATION = 'music_streaming.wsgi.application'
ASGI_APPLICATION = 'music_streaming.asgi.application'

# 6) Database: usa sempre DATABASE_URL iniettata da Railway
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=not DEBUG
    )
}

# 7) Internationalization, static, ecc.
LANGUAGE_CODE = 'it-it'
TIME_ZONE     = 'Europe/Rome'
USE_I18N      = True
USE_TZ        = True

STATIC_URL       = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 8) Auth URLs
AUTH_USER_MODEL     = 'accounts.User'
LOGIN_URL           = 'accounts:login'
LOGIN_REDIRECT_URL  = 'music:song-list'
LOGOUT_REDIRECT_URL = 'accounts:login'
