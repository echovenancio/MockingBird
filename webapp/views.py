from django.shortcuts import render, HttpResponse, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.validators import validate_email
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as dlogin
from django.core.mail import send_mail
from webapp.utils import run_user_code
from . import forms
from . import models
from .decorators import login_verified

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
                dlogin(request, user)
            return redirect("app:signup-confirmation")
    return render(request, "webapp/signup.html", {"form": form})

@login_required
def signup_confirmation(request):
    if request.method == "POST":
        user = request.user
        if user.is_verified:
            return redirect("app:dashboard")
        pin = request.POST.get("pin", "")
        try:
            ticket = models.VerificationTicket.objects.get(user=user)
            if str(ticket.pin) == str(pin):
                user.is_verified = True
                user.save()
                ticket.delete()
                return redirect("app:dashboard")
            else:
                return render(request, "webapp/confirmation.html", {"pin": pin, "error": "pin incorreto."})
        except models.VerificationTicket.DoesNotExist:
            return HttpResponse("ué")
    return render(request, "webapp/confirmation.html", {})

def login(request):
    form = forms.LoginForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                dlogin(request, user)
                return redirect("app:dashboard")
    return render(request, "webapp/login.html", {"form": form})

def password_recovery(request):
    if request.POST:
        email = request.POST.get("email", "")
        try:
            validate_email(email)
            user = models.User.objects.get(email=email)
            ticket = models.PasswordRecoveryTicket(user=user)
            url = f"0.0.0.0:8000{reverse('app:password-recovery-confirmation', args=(ticket.token,))}"
            ticket.save()
            send_mail(
                "Recuperação de senha",
                f"url de recuperação de senha: {url}",
                "mockingbird@email.com",
                [email],
            )
        except ValidationError:
            return render(request, "webapp/accounts/password_recovery.html", {"email": email, "error": "email inválido."})
        except models.User.DoesNotExist:
            pass
        return render(request, "webapp/accounts/password_recovery_done.html", {})
    return render(request, "webapp/accounts/password_recovery.html", {})

def password_recovery_confirmation(request, token):
    form = forms.NewPasswordForm(request.POST or None)
    ticket = get_object_or_404(models.PasswordRecoveryTicket, token=token)
    if request.POST:
        if form.is_valid():
            ticket = models.PasswordRecoveryTicket.objects.get(token=token)
            user = ticket.user 
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            ticket.delete()
            messages.success(request, "Senha atualizada!")
            return redirect("app:login")
    return render(request, "webapp/accounts/password_recovery_confirm.html", {"form": form, "token": token})

@login_verified
def dashboard(request):
    return(HttpResponse("boa"))

def run_code(request):
    if request.POST:
        response = run_user_code("tests/test_add.lua", request.POST.get("code", "")) 
        print(response)
        return HttpResponse(response)
    else:
        return render(request, "webapp/test_code.html")
