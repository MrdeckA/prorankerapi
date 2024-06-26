"""
Django settings for prorankersapi project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


AUTH_USER_MODEL = 'user.User'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-agq*xe10=sjzi#f*&%dw(xenu#-s)ju3cm*yhht^ifyn45ha!r"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1',]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'user',
    'campagne',
    'candidat',
    'collaboration',
    'rest_framework_simplejwt',
    'corsheaders',


    
]




REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': ('user.authentication.JWTAuthentication',),
     'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Durée de validité du token
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # Durée de validité pour la mise à jour du token
    'SLIDING_TOKEN_LIFETIME': timedelta(days=7),  # Durée de validité du token mis à jour
    'SLIDING_TOKEN_REFRESH_DELTA': timedelta(days=6),  # Période de renouvellement du token
    'ROTATE_REFRESH_TOKENS': False,  # Pour renouveler les tokens de rafraîchissement
    'ALGORITHM': 'HS256',  # Algorithme de chiffrement
    'SIGNING_KEY': SECRET_KEY,  # Clé secrète
    'VERIFYING_KEY': None,  # Clé de vérification
}

JWT_CONF = {'TOKEN_LIFETIME_HOURS': 1}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = "prorankersapi.urls"



CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True  # Autorise toutes les origines (à ajuster en production)
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8000",

)


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8000",
]



TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "prorankersapi.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'proranker',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',  # Ou l'adresse IP de votre serveur PostgreSQL
        'PORT': '5432',  # Port par défaut de PostgreSQL
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "uploads/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


STATICFILES_DIRS = [
    BASE_DIR / "uploads",
]



# Configuration de l'envoi d'e-mails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Serveur SMTP de Gmail
EMAIL_PORT = 587  # Port SMTP de Gmail (TLS)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mrdeck30@gmail.com'  # Votre adresse e-mail Gmail
EMAIL_HOST_PASSWORD = 'sytu ssdq hbim islx'  # Mot de passe de votre compte Gmail

# Configuration de l'expéditeur par défaut
DEFAULT_FROM_EMAIL = '<mrdeck30@gmail.com>'