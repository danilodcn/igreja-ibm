from _pytest.doctest import DoctestItem
import pytest
from django.core.management import call_command

NAMES = [
    "igreja.apps.core.utils.utils.get_admin_url",
    "igreja.apps.account.managers",
]


def pytest_collection_modifyitems(items: list[DoctestItem]):
    for _, item in enumerate(items):
        for name in NAMES:
            if name in item.name:
                item.add_marker("django_db")

    call_command("migrate")


@pytest.fixture(scope="session")
def django_db_setup(settings):
    print(settings.DATABASES)

    settings.DATABASES["default"] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
    print(settings.DATABASES)