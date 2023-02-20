from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect

from igreja.apps.account.models import CustomUser
from igreja.apps.core.utils.redirect import get_redirect
from igreja.apps.web.views.accounts.forms import CustomUserForm, LoginForm

from ..base_views import FormBaseView


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


class AccountLoginView(AccountFormBaseView):
    template_name = "registration/login.html"
    success_url = "/"
    form_class = LoginForm

    def form_valid(self, form) -> HttpResponse:
        email = self.request.POST["email"]
        password = self.request.POST["password"]
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


@login_required(login_url="/accounts/login/")
def user_logout(request: HttpRequest):
    logout(request)
    url = get_redirect(request.GET)
    return redirect(url or "/")
