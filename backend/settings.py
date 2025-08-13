"""
Django settings for backend project.
"""

import os
from pathlib import Path
from ctypes.util import find_library
from corsheaders.defaults import default_headers
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Render-specific GDAL setup
# =========================
if os.environ.get("RENDER") or os.environ.get("IS_RENDER"):  # set in Render env
    gdal_lib = find_library("gdal")
    if gdal_lib:
        os.environ["GDAL_LIBRARY_PATH"] = gdal_lib
    else:
        raise RuntimeError("GDAL library not found on Render!")

# =========================
# Security
# =========================
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-dev-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = ["*"]  # Consider restricting to prod domain later

# =========================
# File storage
# =========================
MEDIA_ROOT = "/var/data/media" if os.environ.get("RENDER") else os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# =========================
# Timezone
# =========================
TIME_ZONE = "Africa/Lagos"
USE_TZ = True

# =========================
# Installed apps
# =========================
INSTALLED_APPS = [
    # Django default apps
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

# =========================
# Middleware
# =========================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

# =========================
# Templates
# =========================
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

# =========================
# Auth
# =========================
AUTH_USER_MODEL = "users.User"

# =========================
# WSGI / ASGI
# =========================
WSGI_APPLICATION = "backend.wsgi.application"
ASGI_APPLICATION = "backend.asgi.application"  # needed for Channels

# =========================
# Database
# =========================
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
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": os.environ.get("POSTGRES_DB", "bistropulse"),
            "USER": os.environ.get("POSTGRES_USER", "postgres"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.environ.get("POSTGRES_HOST", "db"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }

# =========================
# Production security
# =========================
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# =========================
# Django REST Framework
# =========================
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

# =========================
# File upload limits
# =========================
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# =========================
# CORS
# =========================
CORS_ALLOWED_ORIGINS = ["http://localhost:4200", "https://bistropulse.vercel.app"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers)
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]

# =========================
# Channels / WebSocket settings
# =========================
REDIS_URL = os.environ.get("REDIS_URL")  # Set by Render Redis service

if REDIS_URL:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [REDIS_URL],
            },
        }
    }
else:
    # fallback to in-memory (local dev)
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }

# =========================
# Optional: Logging / Debugging Channels
# =========================
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'INFO',
#     },
# }
