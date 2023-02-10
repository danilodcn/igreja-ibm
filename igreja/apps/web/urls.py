from django.urls import path

from igreja.apps.web.views import home, accounts

urlpatterns = [
    path("", home.home, name="home"),
    path("church/<slug:slug>", home.home, name="home"),

    path("accounts/create", accounts.CreateUserView.as_view(), name="create-account")
]
