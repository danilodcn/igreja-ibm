from _pytest.doctest import DoctestItem
import pytest

NAMES = [
    "igreja.apps.core.utils.utils.get_admin_url",
    "igreja.apps.account.managers",
]


def pytest_collection_modifyitems(items: list[DoctestItem]):
    for _, item in enumerate(items):
        for name in NAMES:
            if name in item.name:
                item.add_marker("django_db")


@pytest.fixture(autouse=True)
def use_dummy_cache_backend(settings):
    print(settings.DATABASES)


@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings
    print(settings.DATABASES)

    settings.DATABASES["default"] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
    print(settings.DATABASES)