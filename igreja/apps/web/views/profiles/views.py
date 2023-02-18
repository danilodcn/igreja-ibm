from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from igreja.apps.account.models import CustomUser
from django.views import View
from .forms import AddressForm, CustomUserForm, ProfileForm
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        ctx = {
            "user": request.user,
            "form": {
                "user": CustomUserForm(instance=request.user),
                "profile": ProfileForm(instance=request.user.profile),
                "address": AddressForm(instance=request.user.profile.address),
            }
        }
        messages.error(request, "houve um erro")
        messages.error(request, "houve outro um erro")
        return render(request, "web/pages/profile.html", context=ctx)

    def post(self, request: HttpRequest) -> HttpResponse:
        request.POST
        # import ipdb; ipdb.set_trace()
        messages.error(request, "houve um erro")
        return HttpResponse()