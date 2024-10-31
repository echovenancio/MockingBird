from django.urls import path, include
from . import views

app_name = "app"

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login", views.login, name="login"),
    path("accounts/signup", views.signup_page, name="signup"),
    path("accounts/signup-confirmation/", views.signup_confirmation, name="signup-confirmation"),
    path("health-check", views.health_check),
]
