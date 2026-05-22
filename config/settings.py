import os
from pathlib import Path

try:
    import environ
except ImportError:
    environ = None

BASE_DIR = Path(__file__).resolve().parent.parent


class SimpleEnv:
    def __call__(self, key, default=None):
        return os.environ.get(key, default)

    def list(self, key, default=None):
        value = os.environ.get(key)
        if value is None:
            return default if default is not None else []
        return [item.strip() for item in value.split(',') if item.strip()]


env = environ.Env(DEBUG=(bool, False)) if environ else SimpleEnv()

# Read .env if exists (local dev), Railway injects vars directly
env_file = os.path.join(BASE_DIR, '.env')
if os.path.isfile(env_file) and environ:
    environ.Env.read_env(env_file)

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-replace-me-in-production-now')
DEBUG = env('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[]) + ['https://*.up.railway.app', 'https://*.railway.app']

# Railway auto-provides RAILWAY_STATIC_URL
RAILWAY_STATIC_URL = os.environ.get('RAILWAY_STATIC_URL', '')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'accounts',
    'core',
    'equipment',
    'map_builder',
    'requests_app',
    'accounting',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'config.wsgi.application'

# ── Database (Railway MySQL via PyMySQL) ────────────────────────────────────
import pymysql
pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':     os.environ.get('MYSQL_DATABASE',  os.environ.get('MYSQLDATABASE', 'railway')),
        'USER':     os.environ.get('MYSQL_USER',       os.environ.get('MYSQLUSER', 'root')),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD',   os.environ.get('MYSQLPASSWORD', '')),
        'HOST':     os.environ.get('MYSQLHOST',        'localhost'),
        'PORT':     os.environ.get('MYSQLPORT',        '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'CONN_MAX_AGE': 60,
    }
}

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ── Static & Media ──────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

# ── Messages ────────────────────────────────────────────────────────────────
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}
