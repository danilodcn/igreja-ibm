from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout
from django import forms
from django.core import validators

from igreja.apps.account.models import Address, CustomUser, Profile


def validate_email_user(email, user: CustomUser):
    exist_another_user = (
        CustomUser.objects.filter(email__exact=email)
        .exclude(pk=user.pk)
        .exists()
    )
    if exist_another_user:
        raise forms.ValidationError("Existe outra conta com esse email")
    return True


class HorizontalFormMixin:
    @property
    def helper(self):
        helper = FormHelper(self)

        helper.form_tag = False
        helper.disable_csrf = True
        helper.form_class = "horizontal-form needs-validation form-horizontal"

        helper.label_class = "col-md-4 col-lg-3 col-form-label"
        helper.field_class = "col-md-8 col-lg-9 form-field"

        helper.error_text_inline = True
        helper.help_text_inline = True
        helper.form_show_labels = True
        return helper


class CheckFormMixin:
    @property
    def helper(self):
        helper = FormHelper(self)

        helper.form_tag = False
        helper.disable_csrf = True

        helper.error_text_inline = True
        helper.help_text_inline = True
        helper.form_show_labels = True
        return helper


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
