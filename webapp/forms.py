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


class NewPasswordForm(forms.Form):
    new_password = forms.CharField(
        label="Nova senha", max_length=32, widget=forms.PasswordInput
    )
    password_confirmation = forms.CharField(
        label="Confirmação nova senha", max_length=32, widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data["new_password"]
        password_confirmation = cleaned_data["password_confirmation"]
        if new_password != password_confirmation:
            self.add_error("password_confirmation", "ambas as senhas devem ser iguais")
