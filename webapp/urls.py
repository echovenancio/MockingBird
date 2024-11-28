from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "app"

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("cursos", views.cursos, name="cursos"),
    path("curso/<int:id>", views.curso, name="curso"),
    path("eventos", views.eventos, name="eventos"),
    path("forum", views.forum, name="forum"),
    path("course/<int:curso_id>/module/<int:module_id>", views.module, name="module"),
    path(
        "register_to_course/<int:curso_id>",
        views.register_to_course,
        name="register-to-course",
    ),
    path(
        "start_module/<int:curso_id>/<int:module_id>",
        views.start_module,
        name="start-module",
    ),
    path(
        "finish_module/<int:curso_id>/<int:module_id>",
        views.finish_module,
        name="finish-module",
    ),
    path("accounts/login/", views.login, name="login"),
    path("accounts/signup/", views.signup_page, name="signup"),
    path(
        "accounts/signup-confirm/",
        views.signup_confirmation,
        name="signup-confirmation",
    ),
    path(
        "accounts/password-recovery", views.password_recovery, name="password-recovery"
    ),
    path(
        "accounts/password-recovery/cofirm/<uuid:token>",
        views.password_recovery_confirmation,
        name="password-recovery-confirmation",
    ),
    path("health-check/", views.health_check),
    path("test-code/", views.run_code),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
