from copy import deepcopy
from typing import Any

from crispy_forms.utils import render_crispy_form
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, resolve_url
from django.views import View

from igreja.apps.account.models import CustomUser

from ..base_views import FormBaseView
from .forms import (
    AddressModelForm,
    CustomUserForm,
    CustomUserModelForm,
    NotificationsAlertsModelForm,
    ProfileModelForm,
)


class ProfileView(LoginRequiredMixin, FormBaseView):
    template_name = "web/pages/profile.html"

    def get_form_class(self):
        return super().get_form_class()

    def get_context_data(self, **kwargs):
        user: CustomUser = self.request.user

        kwargs["form"] = {
            # "user": CustomUserForm(instance=self.request.user),
            "user": CustomUserForm(
                initial={
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            ),
            "profile": ProfileModelForm(instance=user.profile),
            "address": AddressModelForm(instance=user.profile.address),
            "notifications": NotificationsAlertsModelForm(
                instance=user.profile
            ),
        }
        return super().get_context_data(**kwargs)

    def post(
        self, request: HttpRequest, *args: str, **kwargs: Any
    ) -> HttpResponse:
        user_form = CustomUserForm(request.POST, request.FILES, request=request)
        profile_form = ProfileModelForm(request.POST, request.FILES)
        address_form = AddressModelForm(request.POST, request.FILES)

        forms = {
            "user": user_form,
            "profile": profile_form,
            "address": address_form,
        }

        is_valid = [form.is_valid() for form in forms.values()]

        if not all(is_valid):
            ctx = {"form": forms}
            ctx["form"]["notifications"] = NotificationsAlertsModelForm(
                instance=request.user.profile
            )
            messages.error(
                request, "parece que houve um erro ao salvar os dados"
            )
            return render(request, "web/pages/profile.html", context=ctx)

        user_form = CustomUserModelForm(
            request.POST, request.FILES, instance=request.user
        )
        profile_form = ProfileModelForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        address_form = AddressModelForm(
            request.POST, request.FILES, instance=request.user.profile.address
        )
        try:
            user_form.save()
            profile_form.save()
            address_form.save()
            message = "as atualizações foram salvas com sucesso"
        except Exception as error:
            message = "Houve um erro!"

        messages.info(request, message)
        return redirect(resolve_url("accounts_profile"))


class SaveNotificationsSettings(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        form = NotificationsAlertsModelForm(request.POST)
        status = 200
        import ipdb; ipdb.set_trace()

        if form.is_valid():
            form = NotificationsAlertsModelForm(
                request.POST, instance=request.user.profile
            )
            form.save()
            success = True
        else:
            status = 406
            success = False

        form_rendered = render_crispy_form(form, context={})
        return JsonResponse(
            {"success": success, "errors": form.errors, "form": form_rendered},
            status=status,
        )
