from pathlib import Path

from envparse import env

env.read_envfile()

SRC_DIR = Path(__file__).resolve().parent.parent


# -----------
# Environment
# -----------

DEBUG = env.bool("DEBUG", default=False)


# --------
# Security
# --------

SECRET_KEY = env.str("SECRET_KEY")


# -------
# Web-app
# -------

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

WSGI_APPLICATION = "katubi.wsgi.application"
ROOT_URLCONF = "katubi.urls"
APPEND_SLASH = True
STRICT_URL_LOOKUPS = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# --------------
# Installed apps
# --------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


# ---------
# Templates
# ---------

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


# -------------
# Language/i18n
# -------------

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
USE_I18N = False
USE_L10N = False
USE_TZ = True


# --------
# Database
# --------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.str("DB_PORT", default="5432"),
    }
}


# -------
# Statics
# -------

STATIC_URL = "/static/"
STATIC_ROOT = env.str("STATIC_ROOT", default=(SRC_DIR / "staticfiles"))


# ---------
# Passwords
# ---------

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
