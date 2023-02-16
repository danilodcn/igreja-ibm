from django.urls import path, include

from igreja.apps.web.views import home
from igreja.apps.web.views.accounts import accounts

urlpatterns = [
    path("", home.home, name="home"),
    path("accounts/create/", accounts.CreateUserView.as_view(), name="create_account"),
    path("accounts/logout/", accounts.user_logout, name="logout"),
    path('accounts/login/', accounts.AccountLoginView.as_view(), name="login"),
]
