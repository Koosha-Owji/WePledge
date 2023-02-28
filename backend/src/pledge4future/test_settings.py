#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings for pledg4future project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str


# Load settings from ./.env file
# load_dotenv("../../.env", verbose=True)
#load_dotenv(find_dotenv())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = BASE_DIR.parent / "static"
MEDIA_ROOT = BASE_DIR.parent / "media"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret! - is set in local .env file
SECRET_KEY = '213'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False #os.environ.get("DJANGO_DEBUG")

ALLOWED_HOSTS = ["http://localhost", "localhost", "http://api.test-pledge4future.heigit.org"]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOWED_ORIGINS = ["http://localhost:3000","https://test-pledge4future.heigit.org"]

CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=30
SECURE_HSTS_INCLUDE_SUBDOMAINS=True

# Application definition
INSTALLED_APPS = [
    'emissions.apps.EmissionsConfig',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "graphene_django",
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "graphql_auth",
    "django_filters",
    "django_extensions",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware"
]

ROOT_URLCONF = "pledge4future.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "./templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "pledge4future.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# local database for development
# DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": os.path.join(BASE_DIR, "db.sqlitedb"),
#    }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "HOST": "db",
        "PORT": 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

AUTH_USER_MODEL = "emissions.CustomUser"

GRAPHENE = {
    "SCHEMA": "emissions.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}

AUTHENTICATION_BACKENDS = [
    "graphql_auth.backends.GraphQLAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

GRAPHQL_JWT = {
    # "JWT_AUTH_HEADER_NAME": "HTTP_Authorization",
    "JWT_AUTH_HEADER_PREFIX": "JWT",
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_EXPIRATION_DELTA": timedelta(hours=24),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.SendPasswordResetEmail",
        "graphql_auth.mutations.PasswordReset",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.VerifyToken",
        "graphql_auth.mutations.RefreshToken",
        "graphql_auth.mutations.RevokeToken",
        "graphql_auth.mutations.VerifySecondaryEmail",
    ],
}

GRAPHQL_AUTH = {
    "LOGIN_ALLOWED_FIELDS": ["email"],
    "REGISTER_MUTATION_FIELDS": [
        "email",
        "first_name",
        "last_name",
    ],
    "REGISTER_MUTATION_FIELDS_OPTIONAL": ["academic_title", "first_name", "last_name"],
    "UPDATE_MUTATION_FIELDS": [
        "first_name",
        "last_name",
        "academic_title"
    ],  # "is_representative", "working_group" - make separate mutation
    "ALLOW_DELETE_ACCOUNT": True,
    "SEND_ACTIVATION_EMAIL": True,
    "ALLOW_LOGIN_NOT_VERIFIED": False,
    "EMAIL_FROM": "no-reply@pledge4future.org",
    "ACTIVATION_PATH_ON_EMAIL": os.getenv("PUBLIC_URL", "https://localhost") + "/activate",
    "PASSWORD_RESET_PATH_ON_EMAIL": os.getenv("PUBLIC_URL", "https://localhost") + "/set-new-password",
    "ACTIVATION_SECONDARY_EMAIL_PATH_ON_EMAIL": os.getenv("PUBLIC_URL", "https://localhost") + "/activate-secondary",
    "PASSWORD_SET_PATH_ON_EMAIL": os.getenv("PUBLIC_URL", "https://localhost") + "/set-password",
}

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = "fill_in"
EMAIL_HOST = "fill_in"
EMAIL_HOST_PASSWORD = 'fill_in'



# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


GRAPH_MODELS = {
    "all_applications": True,
    "group_models": True,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}