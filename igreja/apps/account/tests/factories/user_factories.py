from factory.django import DjangoModelFactory
import factory


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = "account.CustomUser"
        django_get_or_create = ("email", "first_name", "last_name")
    
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")