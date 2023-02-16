from typing import Any
from django.views.generic.edit import FormView
from django.views import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django import forms
from igreja.apps.account.models import CustomUser
from django.contrib import messages
from django.contrib.messages.api import get_messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from igreja.apps.web.views.accounts.forms import CustomUserForm,  LoginForm
from igreja.apps.core.utils.redirect import get_redirect



class FormBaseView(FormView):
    def form_invalid(self, form) -> HttpResponse:
        for errors in form.errors.values():
            for msg in errors:
                messages.error(self.request, msg)
        return super().form_invalid(form)
    
    def get_success_url(self) -> str:
        url = get_redirect(self.request.GET)
        if url:
            return url
        return super().get_success_url()


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
            last_name=last_name
        )
        return super().form_valid(form)
    


class AccountLoginView(AccountFormBaseView):
    template_name = "registration/login.html"
    success_url = "/"
    form_class = LoginForm

    def form_valid(self, form) -> HttpResponse:
        email = self.request.POST['email']
        password = self.request.POST['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


@login_required(login_url='/accounts/login/')
def user_logout(request: HttpRequest):
    logout(request)
    url = get_redirect(request.GET)
    return redirect(url or "/")
