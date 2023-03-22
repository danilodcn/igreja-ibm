from _pytest.doctest import DoctestItem, DoctestModule
from pytest import mark, hookimpl


NAMES = [
    "igreja.apps.core.utils.utils.get_admin_url",
]

def pytest_collection_modifyitems(items):
    for i, item in enumerate(items):
        for name in NAMES:
            if name in item.name:
                item.add_marker("django_db")
