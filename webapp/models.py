from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    is_verified = models.BooleanField(default=False)


class VerificationTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6)


class PasswordRecoveryTicket(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=255)


class UserCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)


class Module(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module_template = models.CharField(max_length=255)


class UserModule(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)


class Challenge(models.Model):
    name = models.CharField(max_length=255)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    description = models.TextField(default="")
    code_prelude = models.TextField()
    test_path = models.CharField(max_length=255)


class UserChallenge(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    solution = models.TextField(default="")


class Board(models.Model):
    name = models.CharField(max_length=255)


class Post(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    original_poster = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    likes = models.IntegerField()
    comment = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField(default="")


class Badge(models.Model):
    name = models.CharField(max_length=255)
    icon = models.FileField(upload_to="badges/")


class UserBadge(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Event(models.Model):
    EPIC = "ep"
    RARE = "ra"
    COMMON = "co"
    DIFFICULTY_CHOICES = {EPIC: "epic", RARE: "rare", COMMON: "common"}
    name = models.CharField(max_length=255)
    difficulty = models.CharField(
        max_length=2, choices=DIFFICULTY_CHOICES, default=COMMON
    )
    icon = models.FileField(upload_to="events/")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, null=True)


class UserEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    solution = models.TextField(default="")
