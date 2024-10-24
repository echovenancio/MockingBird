from django.urls import path, include
from . import views

app_name = "app"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup_page, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup-confirmation/", views.signup_confirmation, name="signup-confirmation"),
    path("health-check", views.health_check),
]
