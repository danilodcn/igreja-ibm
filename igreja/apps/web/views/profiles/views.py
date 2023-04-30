from copy import deepcopy
from typing import Any

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, resolve_url

from igreja.apps.account.models import CustomUser
from igreja.apps.web.views.base_views import AjaxView, FormBaseView
from igreja.apps.web.views.profiles.forms import (
    AddressModelForm,
    ChangePasswordForm,
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
            "change_password": ChangePasswordForm(),
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
            ctx["change_password"] = ChangePasswordForm()
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


class SaveNotificationsSettings(LoginRequiredMixin, AjaxView):
    form_class = NotificationsAlertsModelForm

    def get_object(self, *args, **kwargs):
        return self.request.user.profile


class SavePassword(LoginRequiredMixin, AjaxView):
    form_class = ChangePasswordForm

    def form_valid(self):
        form = self.get_form()
        password = self.request.POST.get("password_1")

        self.request.user.set_password(password)

        return form
    
    def get_form(self, *args, **kwargs):
        return super().get_form(request=self.request)
