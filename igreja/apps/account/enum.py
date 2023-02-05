from django.db.models import enums


class UserInteractionCategoriesChoices(enums.TextChoices):
    USER_CREATED = "USER_CREATED", "usuário criado"
    POST_READ = "POST_READ", "usuário viu publicação"
    POST_LIKE = "POST_LIKE", "usuário curtiu publicação"
    EVENT_VIEW = "EVENT_VIEW", "usuário viu um evento"
    EVENT_LIKE = "EVENT_LIKE", "usuário viu um evento"
    BIBLE_VIEW = "BIBLE_VIEW", "usuário viu bíblia"


class ContactMeanTypesChoices(enums.IntegerChoices):
    WHATSAPP = 1, "WhatsApp"
    EMAIL = 2, "email"
    FACEBOOK = 3, "facebook"
    INSTAGRAM = 4, "instagram"
    PHONE = 5, "telefone"
