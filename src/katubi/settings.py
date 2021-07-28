import sys
from pathlib import Path

import sentry_sdk
import structlog
from django.core.management.utils import get_random_secret_key
from envparse import env
from sentry_sdk.integrations.django import DjangoIntegration

env.read_envfile()

SRC_DIR = Path(__file__).resolve().parent.parent


# -----------
# Environment
# -----------

DEBUG = env.bool("DEBUG", default=False)

# --------
# Security
# --------

# This uses a random secret key if none is set. This allows us to run collectstatic
# during the build process without setting a secret key. Beware using any command that
# requires a consistent secret key.
SECRET_KEY = env.str("SECRET_KEY", default=get_random_secret_key())


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
    "django_structlog.middlewares.RequestMiddleware",
]


# --------------
# Installed apps
# --------------

INSTALLED_APPS = [
    "katubi.reading_events",
    "katubi.volumes",
    "katubi.books",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
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
        "NAME": env.str("DB_NAME", default=""),
        "USER": env.str("DB_USER", default=""),
        "PASSWORD": env.str("DB_PASSWORD", default=""),
        "HOST": env.str("DB_HOST", default=""),
        "PORT": env.str("DB_PORT", default="5432"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# -------
# Logging
# -------


def _json_console_handler(level: str) -> dict:
    """
    Build a JSON handler for logging in production.
    """
    return {
        "class": "logging.StreamHandler",
        "stream": sys.stdout,
        "formatter": "json",
        "filters": ["require_debug_false"],
        "level": level,
    }


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "pretty": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
    },
    "handlers": {
        "pretty_console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "pretty",
            "filters": ["require_debug_true"],  # for development
            "level": "DEBUG",
        },
        "json_console_info": _json_console_handler("INFO"),
        "json_console_warning": _json_console_handler("WARNING"),
        "json_console_error": _json_console_handler("ERROR"),
    },
    "loggers": {
        "django": {
            "handlers": ["json_console_error", "pretty_console"],
            "level": "INFO",
            "propagate": False,
        },
        "django_structlog": {
            "handlers": ["json_console_warning", "pretty_console"],
            "level": "INFO",
            "propagate": False,
        },
        "katubi": {
            "handlers": ["json_console_info", "pretty_console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


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


# ------
# Sentry
# ------

# SENTRY_DSN, SENTRY_ENVIRONMENT, and SENTRY_RELEASE will be read from the environment.
sentry_sdk.init(
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)


# ---------------------
# Django REST Framework
# ---------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
