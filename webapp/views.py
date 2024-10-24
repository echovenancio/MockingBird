from django.shortcuts import render, HttpResponse, redirect
from django.core.mail import send_mail
from . import forms


# Create your views here.
def index(request):
    return render(request, "webapp/index.html", {})


def health_check(request):
    return HttpResponse("ok")


def signup_page(request):
    form = forms.RegistrationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            send_mail(
                "Confirmação de email",
                "Codigo ai man",
                "mockingbird@email.com",
                [form.cleaned_data["email"]],
            )
            return redirect("app:signup-confirmation")
    return render(request, "webapp/signup.html", {"form": form})


def signup_confirmation(request):
    return render(request, "webapp/confirmation.html", {})
