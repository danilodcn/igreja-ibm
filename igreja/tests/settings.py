from igreja.settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
        "TEST": {
            "NAME": "test.sqlite3",
        },
    }
}
