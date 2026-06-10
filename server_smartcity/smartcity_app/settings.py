import os
from pathlib import Path
from datetime import timedelta
import psycopg2

# Path Dasar Proyek
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-((em28vx0#y9zqv#0#_&^e5lv1z28e!_9(va5oh3n=uz2!31ny'

DEBUG = True

ALLOWED_HOSTS = ['*']

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
    
    # REST Framework - Lab 9
    'rest_framework',
    # Local API apps for Lab 10
    'reports',
    'usermanagement',
    'rest_framework_simplejwt',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smartcity_app.urls'

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

WSGI_APPLICATION = 'smartcity_app.wsgi.application'

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
STATIC_ROOT = BASE_DIR / 'staticfiles'

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

# CORS settings for local SPA testing and production APIs
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# AUTH MODEL SAFE
AUTH_USER_MODEL = 'usermanagement_24782077.User'

# Django REST Framework + Simple JWT configuration (Lab 10)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}