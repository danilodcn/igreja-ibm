from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from igreja.apps.account.models import (
    Address,
    ContactMeans,
    CustomUser,
    Profile,
    UserInteraction
)


class ContactMeansInlineAdmin(admin.TabularInline):
    search_fields = ["type", "contact"]
    model = ContactMeans
    extra = 0


class AddressAdmin(admin.ModelAdmin):
    list_filter = ["state", "address_type"]
    search_fields = ["city", "state", "zipcode", "country"]
    list_per_page = 50


class ProfileAdminInline(admin.StackedInline):
    model = Profile
    autocomplete_fields = ["address"]


class UserInteractionAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ["__str__", "source", "created_at"]


class CustomUserAdmin(UserAdmin):
    list_display = [
        "__str__",
        "email",
        "get_full_name",
        "is_active",
        "last_login",
    ]
    list_display_links = ["__str__", "email"]
    list_filter = [
        "groups",
    ]
    inlines = [ProfileAdminInline, ContactMeansInlineAdmin]
    filter_horizontal = ["groups", "user_permissions"]
    search_fields = ["first_name", "last_name", "email"]
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


admin.site.register(Address, AddressAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserInteraction, UserInteractionAdmin)
