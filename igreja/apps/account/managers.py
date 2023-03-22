from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        """
        método usado para criar e atribuir uma senha a um usuário
        Examples:
            >>> from igreja.apps.account.models import CustomUser
            >>> CustomUser.objects.all().count() # retorna o número de usuários na base da dados
            0
            >>> user = CustomUser.objects.create_user('meu@email.com', 'password')
        """
        if not email:
            raise ValueError(_("Email is required"))

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        if password:
            user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True

        self.create_user(email, password, **kwargs)

    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)
