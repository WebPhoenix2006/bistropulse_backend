"""
Django settings for backend project.
"""

import os
import platform
import sys

from pathlib import Path
from corsheaders.defaults import default_headers
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


import os

# ⛰️ GIS Required Paths (Updated for Windows local dev)
os.environ[
    "PATH"
] += r";C:\WebPhoenix\bistropulse_backend\.venv\Lib\site-packages\osgeo"

# 👇 This should point directly to the GDAL DLL inside your venv
GDAL_LIBRARY_PATH = (
    r"C:\WebPhoenix\bistropulse_backend\.venv\Lib\site-packages\osgeo\gdal.dll"
)

# Optional but helpful if you're using projections or certain geospatial transforms
os.environ["PROJ_LIB"] = (
    r"C:\WebPhoenix\bistropulse_backend\.venv\Lib\site-packages\osgeo\data\proj"
)
os.environ["GDAL_DATA"] = (
    r"C:\WebPhoenix\bistropulse_backend\.venv\Lib\site-packages\osgeo\data\gdal"
)

# If you're using GEOS (optional, for spatial lookups etc.)
GEOS_LIBRARY_PATH = (
    r"C:\WebPhoenix\bistropulse_backend\.venv\Lib\site-packages\osgeo\geos_c.dll"
)


# Security
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-dev-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = ["*"]

# File storage
MEDIA_ROOT = (
    "/var/data/media" if os.environ.get("RENDER") else os.path.join(BASE_DIR, "media")
)
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

TIME_ZONE = "Africa/Lagos"
USE_TZ = True

# Apps
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    # Third-party apps
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "channels",
    "drf_spectacular",
    # Your apps
    "authapp",
    "restaurants",
    "customers",
    "users",
    "chat",
    "orders",
    "franchise",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

AUTH_USER_MODEL = "users.User"

WSGI_APPLICATION = "backend.wsgi.application"

# Database
RENDER = os.environ.get("RENDER")

if RENDER:
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600, engine="django.contrib.gis.db.backends.postgis"
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

# Security for prod
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Bistropulse Api 🚀",
    "DESCRIPTION": "Bistropulse Backend API endpoints 😊",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# Upload limits
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# CORS
CORS_ALLOWED_ORIGINS = ["http://localhost:4200", "https://bistropulse.vercel.app"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers)
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]

# Channels
ASGI_APPLICATION = "backend.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
