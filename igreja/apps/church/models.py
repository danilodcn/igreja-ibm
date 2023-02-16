from ckeditor.fields import RichTextField
from django.db import models
from ordered_model.models import OrderedModel

from igreja.apps.account.models import Address, CustomUser

    


class MemberType(OrderedModel):
    name = models.CharField("Nome", max_length=100, null=True, blank=True)
    description = RichTextField("Descrição", null=True, blank=True)
    code = models.CharField(
        "Código",
        max_length=30,
        unique=True,
        help_text="Usado para identificar o tipo de membro",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "church_member_type"
        verbose_name = "Tipo de membro"
        verbose_name_plural = "Tipos de membros"

    def __str__(self) -> str:
        return self.name or " - "

    


class ChurchMinistry(OrderedModel):
    name = models.CharField("Nome", max_length=100, null=True, blank=True)
    description = RichTextField("Descrição", null=True, blank=True)
    code = models.CharField(
        "Código",
        max_length=30,
        unique=True,
        help_text="Usado para identificar o ministério",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "church_church_ministry"
        verbose_name = "Ministério da Igreja"
        verbose_name_plural = "Ministérios da Igreja"

    def __str__(self) -> str:
        return self.name or " - "


class Church(models.Model):
    name = models.CharField("Nome", max_length=100, help_text="Nome da igreja")
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        verbose_name="Endereço",
        null=True,
        blank=True,
    )
    code = models.CharField(
        "Código",
        max_length=30,
        unique=True,
        help_text="Usado para identificar a igreja",
        null=True,
        blank=True,
    )
    is_default = models.BooleanField(
        "Igreja sede?", default=False, null=True, blank=True
    )
    active = models.BooleanField("Ativa", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Igreja"
        verbose_name_plural = "Igrejas"

    def __str__(self) -> str:
        return self.name or " - "


class Ministry(models.Model):
    leader = models.ForeignKey(
        CustomUser, models.CASCADE, verbose_name="Líder", null=True, blank=True
    )
    name = models.CharField(
        "Nome do lider", max_length=100, null=True, blank=True
    )
    church = models.ForeignKey(Church, models.CASCADE, verbose_name="Igreja")
    ministry = models.ForeignKey(
        ChurchMinistry,
        models.CASCADE,
        verbose_name="Ministério da Igreja",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ministério"
        verbose_name_plural = "Ministérios"

    def __str__(self) -> str:
        return "{} {}".format(self.church, self.leader)


class Member(models.Model):
    member = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Membro",
        related_name="member",
    )
    member_type = models.ForeignKey(
        MemberType, on_delete=models.CASCADE, verbose_name="Tipo de membro"
    )

    church = models.ForeignKey(
        Church,
        on_delete=models.CASCADE,
        verbose_name="Igreja",
        related_name="members",
    )

    class Meta:
        verbose_name = "Membro"
        verbose_name_plural = "Membros"
