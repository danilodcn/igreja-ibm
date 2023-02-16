from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from igreja.apps.account.models import CustomUser
from django.views import View
from ..base_views import FormBaseView

from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "web/pages/profile.html")
