from _pytest.doctest import DoctestItem

NAMES = [
    "igreja.apps.core.utils.utils.get_admin_url",
    "igreja.apps.account.managers",
]


def pytest_collection_modifyitems(items: list[DoctestItem]):
    for _, item in enumerate(items):
        for name in NAMES:
            if name in item.name:
                item.add_marker("django_db")
