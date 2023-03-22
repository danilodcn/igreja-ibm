from igreja.apps.account.models import CustomUser
from faker import Faker
import pytest
import secrets


fake = Faker()


def test_create_simple_user_return_custom_user(db):
    user = CustomUser.objects.create_user(
        email=fake.email(),
        password=secrets.token_bytes(),
    )
    assert isinstance(user, CustomUser)


def test_create_superuser_return_custom_user(db):
    user = CustomUser.objects.create_superuser(
        email=fake.email(),
        password=secrets.token_bytes(),
    )
    assert isinstance(user, CustomUser)


def test_create_simple_user_without_email(db):
    with pytest.raises(ValueError) as error:
        CustomUser.objects.create_user(email=None)

    assert str(error.value) == "Email is required"


def test_create_simple_user_with_password(db):
    password = secrets.token_hex()
    user: CustomUser = CustomUser.objects.create_user(
        email=fake.email(),
        password=password
    )

    assert user.password and user.password != password


def test_create_super_user_without_email(db):
    with pytest.raises(ValueError) as error:
        CustomUser.objects.create_superuser(email=None)

    assert str(error.value) == "Email is required"


def test_create_super_user_with_password(db):
    password = secrets.token_hex()
    user: CustomUser = CustomUser.objects.create_superuser(
        email=fake.email(),
        password=password
    )

    assert isinstance(user, CustomUser)
    assert user.password and user.password != password


def test_find_user_using_upper_case(create_user):
    user, *_ = create_user(1)
    user.email = user.email.lower()
    user.save()
    query = CustomUser.objects.filter(email=user.email.upper())
    assert query.exists() and query.count() == 1


def test_find_user_using_lower_case(create_user):
    user, *_ = create_user(1)
    user.email = user.email.upper()
    user.save()
    query = CustomUser.objects.filter(email=user.email.lower())
    assert query.exists() and query.count() == 1
