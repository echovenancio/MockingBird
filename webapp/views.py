from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib.auth.models import User
from . import forms
from . import models


# Create your views here.
def index(request):
    return render(request, "webapp/index.html", {})


def health_check(request):
    return HttpResponse("ok")


def signup_page(request):
    import secrets

    form = forms.RegistrationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            if not User.objects.filter(email=email):
                user = form.save()
                pin = "".join([str(secrets.randbelow(10)) for _ in range(6)])
                ticket = models.VerificationTicket(user=user, pin=pin)
                ticket.save()
                send_mail(
                    "Confirmação de email",
                    f"código de confirmação do email: {pin}",
                    "mockingbird@email.com",
                    [email],
                )
                request.session["user_id"] = user.id
            return redirect("app:signup-confirmation")
    return render(request, "webapp/signup.html", {"form": form})


def signup_confirmation(request):
    if request.method == "POST":
        user_id = request.session["user_id"]
        pin = request.POST.get("pin", "")
        if user_id is not None and pin != "":
            print("ta massa")
            user = User.objects.get(pk=request.session["user_id"])
            print(user.email)
            print(pin)
            try:
                ticket = models.VerificationTicket.objects.get(user=user)
                if sre(ticket.pin) == str(pin):
                    print("boa")
                    verified_group = Group.objects.get(name="verified_group")
                    user.groups.add(verified_group)
                return HttpResponse("Registrado")
            except models.VerificationTicket.DoesNotExist:
                return HttpResponse("ué")
    return render(request, "webapp/confirmation.html", {})
