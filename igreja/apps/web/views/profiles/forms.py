from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import validators

from igreja.apps.account.models import Address, CustomUser, Profile
from igreja.apps.core.forms.form_base import CheckFormMixin, HorizontalFormMixin


def validate_email_user(email, user: CustomUser):
    exist_another_user = (
        CustomUser.objects.filter(email__exact=email)
        .exclude(pk=user.pk)
        .exists()
    )
    if exist_another_user:
        raise forms.ValidationError("Existe outra conta com esse email")
    return True


class CustomUserForm(HorizontalFormMixin, forms.Form):
    email = forms.CharField(
        required=True, validators=[validators.validate_email]
    )
    first_name = forms.CharField(required=True, label="Nome")
    last_name = forms.CharField(required=True, label="Sobrenome")

    def __init__(self, *args, request=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_email(self):
        email_cleaned = self.cleaned_data.get("email")
        if self.request and isinstance(self.request.user, CustomUser):
            validate_email_user(email_cleaned, self.request.user)

        return email_cleaned


class CustomUserModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]


class ProfileModelForm(HorizontalFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "image",
            "about",
            "gender",
            "cpf",
            "rg",
            "phone",
            "birth_date",
            "occupation",
            "marital_status",
        )


class AddressModelForm(HorizontalFormMixin, forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "country",
            "state",
            "city",
            "zipcode",
            "street",
            "neighborhood",
            "number",
            "complement",
        )


class ChangePasswordForm(HorizontalFormMixin, forms.Form):
    current = forms.CharField(
        label="Senha atual",
        max_length=100,
        required=True,
    )
    password_1 = forms.CharField(
        label="Nova senha",
        max_length=100,
        required=True,
    )
    password_2 = forms.CharField(
        label="Confirmação de senha",
        max_length=100,
        required=True,
    )

    def __init__(self, *args, **kwargs) -> None:
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_current(self):
        current_cleaned = self.data.get("current")

        if not self.request:
            raise forms.ValidationError("Erro interno!")

        if self.request and self.request.user.pk:
            user = authenticate(
                self.request,
                email=self.request.user.email,
                password=current_cleaned,
            )
            if not user:
                raise forms.ValidationError("Senha incorreta!")

        return current_cleaned

    def clean_password(
        self,
    ):
        pass1 = self.data.get("password_1", None)
        pass2 = self.data.get("password_2", None)
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("As senhas não são iguais")

        if not self.request:
            raise forms.ValidationError("Erro interno!")

        validate_password(pass1, user=self.request.user)

    def clean_password_1(self):
        pass1 = self.data.get("password_1", None)
        self.clean_password()

        return pass1


class NotificationsAlertsModelForm(CheckFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "new_products_alerts",
            "new_posts_alerts",
            "new_events_alerts",
            "security_alerts",
        ]

    def clean_security_alerts(self):
        security_alerts_cleaned = self.cleaned_data.get("security_alerts")
        if not security_alerts_cleaned:
            raise forms.ValidationError("Esse campo é obrigatório")
        return security_alerts_cleaned
