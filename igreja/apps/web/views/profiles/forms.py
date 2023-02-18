from django import forms
from crispy_forms.helper import FormHelper
from igreja.apps.account.models import Address, CustomUser, Profile


class HorizontalFormMixin:
    form_id: str | None = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = self.form_id or "id-{}-form".format(
            self.instance.__class__.__name__.lower()
        )
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4 col-lg-3 col-form-label'
        self.helper.field_class = 'col-md-8 col-lg-9'


class CustomUserForm(HorizontalFormMixin, forms.ModelForm): 

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]
        labels = {
            "email": "Email",
            "first_name": "Nome",
            "last_name": "Sobrenome"
        }


class ProfileForm(HorizontalFormMixin, forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'image', "biography", "gender", "cpf", "rg", "phone", "occupation", "marital_status")
        labels = {
            "image": "Perfil",
            "biography": "Sobre",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image_field = self.fields["image"]


class AddressForm(HorizontalFormMixin, forms.ModelForm):

    class Meta:
        model = Address
        fields = ('country', 'state', "city", "zipcode", "street")