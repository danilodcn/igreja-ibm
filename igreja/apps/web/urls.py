from django.urls import path

from igreja.apps.web.views import home

urlpatterns = [
    path("", home.home, name="home"),
    path("church/<slug:slug>", home.home, name="home"),
]
