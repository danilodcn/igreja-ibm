from _pytest.doctest import DoctestItem
import pytest
from django.core.management import call_command

NAMES = [
    "igreja.apps.core.utils.utils.get_admin_url",
    "igreja.apps.account.managers",
]


@pytest.fixture(autouse=True)
def set_global_state():
    ...

def pytest_collection_modifyitems(items: list[DoctestItem]):
    for _, item in enumerate(items):
        for name in NAMES:
            if name in item.name:
                from django.conf import settings
                print(settings.DATABASES)
                item.add_marker("django_db")

    # call_command("migrate")
