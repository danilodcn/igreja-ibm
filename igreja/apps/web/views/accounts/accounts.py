from typing import Any
from django.views.generic.edit import FormView
from django.views import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django import forms
from igreja.apps.account.models import CustomUser
from django.contrib import messages
from django.contrib.messages.api import get_messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from igreja.apps.web.views.accounts.forms import CustomUserForm
from igreja.apps.core.utils.redirect import get_redirect




class CreateUserView(FormView):
    template_name = "web/pages/accounts/create.html"
    success_url = "/"
    form_class = CustomUserForm
    queryset = CustomUser.objects.filter()

    def form_valid(self, form) -> HttpResponse:
        import ipdb; ipdb.set_trace()
        user = form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form) -> HttpResponse:
        for errors in form.errors.values():
            for msg in errors:
                messages.error(self.request, msg)
        return super().form_invalid(form)


@login_required(login_url='/accounts/login/')
def user_logout(request: HttpRequest):
        import ipdb; ipdb.set_trace()
        logout(request)
        url = get_redirect(request.GET)
        return redirect(url)
