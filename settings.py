import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Disable AVX for TensorFlow on M1
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = "your-secret-key"

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = True  # Set to False in production

# Allowed Hosts
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Dataset Paths
DATASETS = {
    "symptom": os.path.join(BASE_DIR, "datasets/data.csv"),
    "skin": os.path.join(BASE_DIR, "datasets/Dogs"),
}

# AI Model Paths
MODELS = {
    "symptom": os.path.join(BASE_DIR, "models/symptom_model.pkl"),
    "vectorizer": os.path.join(BASE_DIR, "models/symptom_vectorizer.pkl"),
    "skin": os.path.join(BASE_DIR, "models/skin_disease_model.h5"),
}

# Installed Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "users",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL Configuration
ROOT_URLCONF = "pet.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# WSGI Application
WSGI_APPLICATION = "pet.wsgi.application"

# Database Configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Authentication Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static Files Configuration
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default Auto Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
