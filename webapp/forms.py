from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = models.User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário", max_length=255)
    password = forms.CharField(label="Senha", max_length=32, widget=forms.PasswordInput)
