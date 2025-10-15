import django.contrib.auth.views as auth_views
import django.urls
import users.views

app_name = "users"
urlpatterns = [
    django.urls.path(
        "login/",
        users.views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    django.urls.path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    django.urls.path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=django.urls.reverse_lazy("users:password_change_done"),
        ),
        name="password_change",
    ),
    django.urls.path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    django.urls.path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            success_url=django.urls.reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    django.urls.path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    django.urls.path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=django.urls.reverse_lazy(
                "users:password_reset_complete",
            ),
        ),
        name="password_reset_confirm",
    ),
    django.urls.path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    django.urls.path("signup/", users.views.SignUpView.as_view(), name="signup"),
    django.urls.path("profile/", users.views.PrivateProfileEditView.as_view(), name="edit-profile"),
    django.urls.path("<str:username>/", users.views.PublicProfileView.as_view(), name="profile"),
]
