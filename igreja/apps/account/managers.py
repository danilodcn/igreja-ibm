from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str | None = None, **kwargs):
        """
        método usado para criar e atribuir uma senha a um usuário

        Attributes:
            email (str): email do usuário a ser criado
            password (str): senha
            **kwargs (dict): atributos adicionais do usuário

        Raises:
            ValueError: Quando o email nao for um email válido

        Examples:
            >>> from igreja.apps.account.models import CustomUser
            >>> CustomUser.objects.all().count() # retorna o número de usuários na base da dados
            0
            >>> user = CustomUser.objects.create_user(email='meu@email.com', password='password')
            >>> user.is_superuser
            False
            >>> new = CustomUser.objects.create_user(email=None, password='password') # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ValueError: ...
        """
        if not email:
            raise ValueError(_("Email is required"))

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        if password:
            user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password: str | None = None, **kwargs):
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True

        return self.create_user(email, password, **kwargs)

    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)

    def filter(self, *args, **kwargs):
        if email := kwargs.pop("email", None):
            kwargs["email__iexact"] = email

        return super().filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        if email := kwargs.pop("email", None):
            kwargs["email__iexact"] = email

        return super().get(*args, **kwargs)
