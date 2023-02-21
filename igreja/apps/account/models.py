from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import FieldTracker

from igreja.apps.account.managers import CustomUserManager

from .enum import ContactMeanTypesChoices, UserInteractionCategoriesChoices


def get_profile_image_upload_to(model, name: str):
    now = timezone.now()
    date = now.strftime("%d/%m/%Y")
    return f"accounts/profile/{model.pk}/{date}/{name}"


class CustomUser(AbstractUser):
    email = models.EmailField(
        "Endereço de email",
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists.")
        },
    )
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.get_full_name()

    @property
    def profile(self):
        profile, _ = Profile.objects.get_or_create(user=self)
        return profile

    @property
    def full_name(self):
        return self.get_full_name()

    def get_full_name(self):
        first_name = self.first_name.strip()
        last_name = self.last_name.strip()

        return "{} {}".format(first_name, last_name).strip()

    def get_image(self):
        profile: Profile = self.profile
        return profile.image

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        self.on_create_user()
        return user

    def on_create_user(self):
        try:
            profile = self.profile

            if not profile.address:
                address = Address.objects.create()
                profile.address = address
                profile.save()

        except Profile.DoesNotExist:
            address = Address.objects.create()
            Profile.objects.create(user=self, address=address)


class Address(models.Model):
    STATE_CHOICES = (
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins"),
    )

    ADDRESS_TYPE_CHOICES = (
        ("alameda", "ALAMEDA"),
        ("avenida", "AVENIDA"),
        ("chacara", "CHACARA"),
        ("condominio", "CONDOMÍNIO"),
        ("conjunto", "CONJUNTO"),
        ("estrada", "ESTRADA"),
        ("ladeira", "LADEIRA"),
        ("largo", "LARGO"),
        ("parque", "PARQUE"),
        ("praca", "PRAÇA"),
        ("praia", "PRAIA"),
        ("quadra", "QUADRA"),
        ("rodovia", "RODOVIA"),
        ("rua", "RUA"),
        ("travessa", "TRAVESSA"),
        ("via", "VIA"),
    )

    class Meta:
        db_table = "account_address"
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    country = models.CharField(
        max_length=50,
        verbose_name="País",
        blank=True,
        null=True,
    )
    state = models.CharField(
        max_length=2,
        verbose_name="Estado",
        choices=STATE_CHOICES,
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Cidade",
        blank=True,
        null=True,
    )
    zipcode = models.CharField(
        max_length=30,
        verbose_name="CEP",
        blank=True,
        null=True,
    )
    street = models.CharField(
        max_length=100,
        verbose_name="Rua",
        blank=True,
        null=True,
    )
    complement = models.CharField(
        max_length=100,
        verbose_name="Complemento",
        blank=True,
        null=True,
    )
    number = models.CharField(
        max_length=30,
        verbose_name="Número",
        blank=True,
        null=True,
    )
    neighborhood = models.CharField(
        max_length=100,
        verbose_name="Bairro",
        blank=True,
        null=True,
    )
    address_type = models.CharField(
        max_length=100,
        choices=ADDRESS_TYPE_CHOICES,
        verbose_name="Tipo de endereço",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        default = "---"
        return "{}, {}, {}/{}".format(
            self.street or default,
            self.number or default,
            self.city or default,
            self.get_state_display() or default,
        )


class ContactMeans(models.Model):
    type_enum = ContactMeanTypesChoices
    type = models.PositiveSmallIntegerField(
        "Tipo", choices=ContactMeanTypesChoices.choices
    )
    contact = models.CharField("Contato", max_length=200)
    is_public = models.BooleanField("Público", default=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Usuário",
        related_name="contact",
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = "Forma de Contato"
        verbose_name_plural = "Formas de Contato"

    def __str__(self) -> str:
        default = "---"
        return "{} - {}".format(
            self.get_type_display() or default, self.contact or default
        )


class Profile(models.Model):
    GENDER_CHOICES = (
        (0, "Masculino"),
        (1, "Feminino"),
    )

    MARITAL_STATUS_CHOICES = (
        ("single", "solteiro"),
        ("married", "casado"),
        ("widower", "viúvo"),
        ("divorced", "divorciado"),
    )

    tracker = FieldTracker()
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="personal_info",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        "Perfil",
        help_text="imagem usada como perfil da conta",
        null=True,
        blank=True,
        upload_to=get_profile_image_upload_to,
    )
    about = models.TextField(
        "Sobre", help_text="breve descrição do usuário", null=True, blank=True
    )
    address = models.OneToOneField(
        Address,
        models.CASCADE,
        related_name="personal_info",
        null=True,
        blank=True,
    )
    gender = models.IntegerField(
        verbose_name="Sexo",
        choices=GENDER_CHOICES,
        default=2,
        blank=True,
        null=True,
    )
    cpf = models.CharField(
        max_length=14,
        verbose_name="CPF",
        blank=True,
        null=True,
    )
    cnh = models.CharField(
        max_length=14,
        verbose_name="CNH",
        blank=True,
        null=True,
    )
    rg = models.CharField(
        max_length=40,
        verbose_name="RG",
        blank=True,
        null=True,
    )
    phone = models.CharField(
        max_length=17,
        verbose_name="Telefone",
        blank=True,
        null=True,
    )
    income_bracket = models.CharField(
        max_length=200,
        verbose_name="Faixa de renda",
        blank=True,
        null=True,
    )
    occupation = models.CharField(
        max_length=100,
        verbose_name="Profissão",
        help_text="A sua profissão atual",
        blank=True,
        null=True,
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de Nascimento",
    )
    marital_status = models.CharField(
        max_length=100,
        choices=MARITAL_STATUS_CHOICES,
        verbose_name="Estado Civil",
        blank=True,
        null=True,
    )
    emitting_organ = models.CharField(
        max_length=100,
        verbose_name="Orgão Emissor",
        blank=True,
        null=True,
    )
    expedition_date = models.DateField(
        verbose_name="Data de Expedição",
        blank=True,
        null=True,
    )
    email_message_enabled = models.BooleanField(
        verbose_name="Aceitar e-mails para comunicação?",
        default=False,
    )
    phone_message_enabled = models.BooleanField(
        verbose_name="Aceitar comunicação de celular",
        default=False,
    )

    security_alerts = models.BooleanField(
        verbose_name="Alertas de segurança",
        default=True,
    )

    new_products_alerts = models.BooleanField(
        verbose_name="informações sobre novos produtos e serviços",
        default=True,
    )

    new_posts_alerts = models.BooleanField(
        verbose_name="informações sobre novos posts do blog",
        default=True,
    )

    new_events_alerts = models.BooleanField(
        verbose_name="informações sobre novos eventos",
        default=True,
    )

    is_main_contact = models.BooleanField(
        verbose_name="É o contato principal",
        default=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "account_profile"
        verbose_name = "Informação Pessoal"
        verbose_name_plural = "Informações Pessoais"

    def __str__(self):
        if self.user:
            return str(self.user)
        return "Usuário não associado"


class UserInteraction(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    category_enum = UserInteractionCategoriesChoices
    category = models.CharField(
        max_length=32,
        editable=False,
        choices=UserInteractionCategoriesChoices.choices,
    )
    source = models.CharField(
        blank=True, null=True, max_length=100, help_text="Origem"
    )

    class Meta:
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["category", "-created_at"]),
        ]
        verbose_name = "Histórico do Usuário"
        verbose_name_plural = "Históricos dos Usuários"

    def __str__(self) -> str:
        return f"{self.pk} - {self.user} - {self.category}"
