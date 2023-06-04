from typing import Any, Dict
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View
from django.shortcuts import redirect

from igreja.apps.account.models import CustomUser
from igreja.apps.core.utils.redirect import get_redirect
from igreja.apps.core.views.ajax_base_view import AjaxViewMixin
from igreja.apps.web.views.accounts.forms import CustomUserForm, LoginForm
from igreja.apps.web.views.base_views import FormBaseView


class AccountFormBaseView(FormBaseView):
    queryset = CustomUser.objects.filter()


class CreateUserView(AccountFormBaseView):
    template_name = "registration/create.html"
    success_url = "/accounts/login"
    form_class = CustomUserForm

    def form_valid(self, form) -> HttpResponse:
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password_1"]

        CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        return super().form_valid(form)



class LoginView(View, AjaxViewMixin):
    form_class = LoginForm

    def form_is_valid(self, form: forms.Form) -> Any:
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            login(self.request, user)
        return user

class AccountLoginView(AccountFormBaseView):
    template_name = "registration/login.html"
    success_url = "/"
    form_class = LoginForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs.update({
            "form": self.get_form()
        })
        return super().get_context_data(**kwargs)
    
    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "request": self.request
        })
        return kwargs
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)


@login_required(login_url="/accounts/login/")
def user_logout(request: HttpRequest):
    logout(request)
    url = get_redirect(request.GET)
    return redirect(url or "/")
