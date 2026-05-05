import os
from pathlib import Path
import psycopg2

# Path Dasar Proyek
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-((em28vx0#y9zqv#0#_&^e5lv1z28e!_9(va5oh3n=uz2!31ny'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']  # Added for development

# Pendaftaran Aplikasi
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom user model harus di atas app lain
    'usermanagement_24782077.apps.Usermanagement24782077Config',
    # apps kamu (FIX: pakai AppConfig)
    'main_app.apps.MainAppConfig',
    'contacts.apps.ContactsConfig',
    'dashboard_24782077.apps.Dashboard24782077Config',  # NEW - Dashboard App
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'npm24782077_iet_2026.urls'

# TEMPLATE CONFIG
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

WSGI_APPLICATION = 'npm24782077_iet_2026.wsgi.application'

# DATABASE SQLITE UNTUK LAB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalisasi
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'   # FIX INDONESIA

USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Messages Bootstrap mapping
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# CSRF Settings for development
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']
CSRF_COOKIE_SECURE = False
CSRF_USE_SESSIONS = False
SESSION_COOKIE_SECURE = False

# AUTH MODEL SAFE
AUTH_USER_MODEL = 'usermanagement_24782077.User'