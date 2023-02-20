import os
from pathlib import Path

from decouple import Csv, config
from dj_database_url import parse as parse_db_url
from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")
SITE_ABSOLUTE_URL = config("SITE_ABSOLUTE_URL")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ckeditor",
    "ckeditor_uploader",
    "crispy_forms",
    "crispy_bootstrap5",
    "import_export",
    "igreja.apps.core",
    "igreja.apps.account",
    "igreja.apps.web",
    "igreja.apps.church",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "igreja.apps.core.middleware.QueryStringMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

from django.middleware.csrf import CsrfViewMiddleware

ROOT_URLCONF = "igreja.urls"

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
                "igreja.apps.core.context.web_context",
            ],
        },
    },
]


MESSAGE_TAGS = {
    message_constants.DEBUG: "debug",
    message_constants.INFO: "info",
    message_constants.SUCCESS: "success",
    message_constants.WARNING: "warning",
    message_constants.ERROR: "danger",
}

WSGI_APPLICATION = "igreja.wsgi.application"

AUTH_USER_MODEL = "account.CustomUser"

SITE_ID = 1

# Database

DATABASES = {
    "default": config(
        "DATABASE_URL",
        default="sqlite:///" + str(BASE_DIR / "db.sqlite3"),
        cast=parse_db_url,
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa
    },
]


def get_cache():
    try:
        servers = config("MEMCACHE_SERVERS", cast=Csv())
        username = config("MEMCACHE_USERNAME")
        password = config("MEMCACHE_PASSWORD")
        return {
            "default": {
                "BACKEND": "django_bmemcached.memcached.BMemcached",
                # TIMEOUT is not the connection timeout!
                #   It's the default expiration
                # timeout that should be applied to keys!
                #   Setting it to `None`
                # disables expiration.
                "TIMEOUT": None,
                "LOCATION": servers,
                "OPTIONS": {
                    "username": username,
                    "password": password,
                },
            }
        }
    except Exception as err:
        return {
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
            }
        }


CACHES = get_cache()

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "staticfiles/"
STATIC_ROOT = BASE_DIR / "staticfiles/statics/"
STATICFILES_DIRS = [
    BASE_DIR / "staticfiles",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_FILENAME_GENERATOR = "igreja.apps.core.utils.utils.get_filename"

CKEDITOR_CONFIGS = {
    "default": {
        # "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Link", "Unlink"],
            ["RemoveFormat", "Source"],
        ],
    },
    "awesome_ckeditor": {
        "toolbar": "Basic",
    },
}


# AWS config

# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
# AWS_REGION_NAME = config("AWS_REGION_NAME")

# AWS_QUERYSTRING_EXPIRE = config("AWS_QUERYSTRING_EXPIRE", 24 * 60 * 60)
# AWS_QUERYSTRING_AUTH = True


CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = CRISPY_TEMPLATE_PACK
