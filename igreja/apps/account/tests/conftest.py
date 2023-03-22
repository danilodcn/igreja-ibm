import pytest
from igreja.apps.account.tests.factories.user_factories import CustomUserFactory


@pytest.fixture
def create_user(db):
    def create_user(n: int):
        return CustomUserFactory.create_batch(n)
    return create_user