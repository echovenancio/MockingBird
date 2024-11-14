from django.urls import path, include
from . import views
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

app_name = "app"

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("accounts/login/", views.login, name="login"),
    path("accounts/signup/", views.signup_page, name="signup"),
    path("accounts/signup-confirm/", views.signup_confirmation, name="signup-confirmation"),
    path("accounts/password-recovery", views.password_recovery, name="password-recovery"),
    path("accounts/password-recovery/cofirm/<uuid:token>", views.password_recovery_confirmation, name="password-recovery-confirmation"),
    path("health-check/", views.health_check),
    path("test-code/", views.run_code),
]
