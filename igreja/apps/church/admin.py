from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Church, ChurchMinistry, Member, MemberType, Ministry


class ContentForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), label="Descrição")


class MemberAdminInline(admin.TabularInline):
    extra = 0
    model = Member
    autocomplete_fields = ["member", "church"]

    model.__str__ = lambda _: ""


class MemberTypeAdmin(ImportExportModelAdmin):
    form = ContentForm
    inlines = [MemberAdminInline]
    search_fields = ["name", "code"]


class ChurchMinistryAdmin(ImportExportModelAdmin):
    form = ContentForm
    search_fields = ["name", "code"]


class MinistryAdmin(ImportExportModelAdmin):
    search_fields = ["name", "code"]
    autocomplete_fields = ["leader", "church", "ministry"]


class ChurchAdminForm(forms.ModelForm):
    class Meta:
        model = Church
        exclude = ["members"]


class ChurchAdmin(ImportExportModelAdmin):
    form = ChurchAdminForm
    list_display = [
        "__str__",
        "is_default",
        "get_members_number",
        "active",
    ]
    autocomplete_fields = ["address"]
    search_fields = ["code", "name"]
    list_per_page = 25

    list_filter = [
        ("address__state", admin.AllValuesFieldListFilter),
    ]

    inlines = [
        MemberAdminInline,
    ]

    @admin.display(description="Número de membros")
    def get_members_number(self, obj: Church):
        return obj.members.all().count()


admin.site.register(MemberType, MemberTypeAdmin)
admin.site.register(ChurchMinistry, ChurchMinistryAdmin)
admin.site.register(Ministry, MinistryAdmin)
admin.site.register(Church, ChurchAdmin)
