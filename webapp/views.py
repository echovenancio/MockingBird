from django.shortcuts import render, HttpResponse, redirect
from django.core.mail import send_mail
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
            if not models.User.objects.filter(email=email):
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
            user = models.User.objects.get(pk=request.session["user_id"])
            print(user.email)
            print(pin)
            try:
                ticket = models.VerificationTicket.objects.get(user=user)
                if str(ticket.pin) == str(pin):
                    print("aqui")
                    user.is_verified = True
                    user.save()
                return HttpResponse("Registrado")
            except models.VerificationTicket.DoesNotExist:
                return HttpResponse("ué")
    return render(request, "webapp/confirmation.html", {})

def login(request):
    form = forms.LoginForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_verified:
                    redirect("app:signup-confirmation")
                else:
                    request.session["user_id"] = user.id
                    return HttpResponse("logado")
    return render(request, "webapp/login.html", {"form": form})
