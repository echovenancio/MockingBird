from django.contrib.auth.forms import ValidationError
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


def about(request):
    return render(request, "webapp/about.html", {})


def contact(request):
    return render(request, "webapp/contact.html", {})


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
    return render(request, "webapp/accounts/signup.html", {"form": form})


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
                return render(
                    request,
                    "webapp/accounts/confirmation.html",
                    {"pin": pin, "error": "pin incorreto."},
                )
        except models.VerificationTicket.DoesNotExist:
            return HttpResponse("ué")
    return render(request, "webapp/accounts/confirmation.html", {})


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
    return render(request, "webapp/accounts/login.html", {"form": form})


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
            return render(
                request,
                "webapp/accounts/password_recovery.html",
                {"email": email, "error": "email inválido."},
            )
        except models.User.DoesNotExists:
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
            user.set_password(form.cleaned_data["new_password"])
            user.save()
            ticket.delete()
            messages.success(request, "Senha atualizada!")
            return redirect("app:login")
    return render(
        request,
        "webapp/accounts/password_recovery_confirm.html",
        {"form": form, "token": token},
    )


@login_verified
def dashboard(request):
    user = request.user
    user_courses = user.usercourse_set.all()
    return render(request, "webapp/user_area/dashboard.html", {"cursos": user_courses})


@login_verified
def cursos(request):
    cursos = models.Course.objects.all()
    return render(request, "webapp/user_area/cursos.html", {"cursos": cursos})


@login_verified
def forum(request):
    boards = models.Board.objects.all()
    return render(request, "webapp/user_area/forum.html", {"boards": boards})


@login_verified
def board(request, board_id):
    board = get_object_or_404(models.Board, pk=board_id)
    posts = models.Board.post_set.filter(comment=None)
    return render(
        request, "webapp/user_area/board.html", {"board": board, "posts": posts}
    )


@login_verified
def poast(request, board_id, post_id):
    post = get_object_or_404(models.Post, pk=post_id)
    comments = post.comment_set.all()
    return render(
        request, "webapp/user_area/post.html", {"post": post, "comments": comments}
    )


@login_verified
def eventos(request):
    eventos = models.Event.objects.all()
    return render(request, "webapp/user_area/eventos.html", {"eventos": eventos})


@login_verified
def curso(request, id):
    try:
        course = models.Course.objects.get(pk=id)
        is_enrolled = False
        modules = None
        if course.usercourse_set.filter(user=request.user).exists():
            is_enrolled = True
            modules = [
                x.module
                for x in models.UserModule.objects.filter(
                    user=request.user, module__course=course
                )
            ]
        else:
            modules = models.Module.objects.filter(course=course)
        return render(
            request,
            "webapp/user_area/curso.html",
            {"course": course, "modules": modules, "enrolled": is_enrolled},
        )
    except models.Course.DoesNotExist:
        return redirect("app:cursos")


@login_verified
def module(request, curso_id, module_id):
    try:
        from pathlib import Path

        user_module = models.UserModule.objects.get(
            user=request.user, module__id=module_id
        )
        file_path = Path(user_module.module.module_template)
        markdown = file_path.read_text()
        return render(
            request,
            "webapp/user_area/module.html",
            {"module": user_module, "markdown": {"inner": markdown}},
        )
    except models.UserModule.DoesNotExist:
        return redirect("app:curso", curso_id)


@login_verified
def get_challenge(request, curso_id, modulo_id):
    challenge = None
    try:
        challenge = models.Challenge.get(module=models.Module.get(pk=modulo_id))
    except models.Challenge.DoesNotExist:
        return redirect("app:cursos")
    return render(request, "webapp/user_area/challenge.html", {"challenge": challenge})


@login_verified
def finish_challenge(request, curso_id, modulo_id):
    if request.POST:
        user = request.user
        challenge = None
        code = request.POST.get("code", "")
        try:
            challenge = models.Challenge.get(module=models.Module.get(pk=modulo_id))
        except models.Challenge.DoesNotExist:
            return redirect("app:cursos")
        result = run_user_code(challenge.test_path, code)
        if result.code == 0:
            user.userchallenge_set.create(
                challenge=challenge, finished=True, solution=code
            )
            user.usermodule_set.get(
                module=models.Module.get(pk=modulo_id)
            ).finished = True
        user.save()
        return redirect("app:modulos")


@login_verified
def get_event(request, event_id):
    event = None
    try:
        event = models.Event.get(pk=event_id)
    except models.Event.DoesNotExist:
        return redirect("app:eventos")
    return render(request, "webapp/user_area/event.html", {"event": event})


@login_verified
def finish_event(request, event_id):
    if request.POST:
        user = request.user
        event = None
        code = request.POST.get("code", "")
        try:
            event = models.Event.get(pk=event_id)
        except models.Event.DoesNotExist:
            return redirect("app:eventos")
        result = run_user_code(event.challenge.test_path, code)
        if result.code == 0:
            user.userevent_set.create(event=event, finished=True, solution=code)
        user.save()
        return redirect("app:eventos")


@login_verified
def register_to_course(request, curso_id):
    if request.POST:
        try:
            course = models.Course.objects.get(pk=curso_id)
            user = request.user
            user.usercourse_set.create(course=course)
            modules = course.module_set.filter()
            for m in modules:
                user.usermodule_set.create(module=m)
            user.save()
            return redirect("app:curso", curso_id)
        except models.Course.DoesNotExist:
            return redirect("app:cursos")


@login_verified
def start_module(request, curso_id, module_id):
    if request.POST:
        try:
            module = models.Module.get(pk=module_id)
            user = request.user
            user.usermodule_set.create(module=module)
            user.save()
            return redirect("app:module", module_id)
        except models.Course.DoesNotExist:
            return redirect("app:curso", curso_id)
