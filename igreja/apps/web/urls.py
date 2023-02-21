from django.urls import include, path

from igreja.apps.web.views import home
from igreja.apps.web.views.accounts import accounts
from igreja.apps.web.views.profiles import views as profile_views

urlpatterns = [
    path("", home.home, name="home"),
    path(
        "accounts/create/",
        accounts.CreateUserView.as_view(),
        name="create_account",
    ),
    path("accounts/logout/", accounts.user_logout, name="logout"),
    path("accounts/login/", accounts.AccountLoginView.as_view(), name="login"),
    path(
        "accounts/profile",
        profile_views.ProfileView.as_view(),
        name="accounts_profile",
    ),
    path(
        "accounts/profile/save-notifications",
        profile_views.SaveNotificationsSettings.as_view(),
        name="accounts_save_notifications",
    ),
]
