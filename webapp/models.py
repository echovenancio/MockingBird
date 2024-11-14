from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group
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

class Module(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module_template = models.CharField(max_length=255)

class Challenge(models.Model):
    name = models.CharField(max_length=255)
    module = models.ForeignKey(Module, on_delte=models.CASCADE)
    code_prelude = models.TextField()
    test_path = models.CharField(max_length=255)

class Board(models.Model):
    name = models.CharField(max_length=255)

class Post(models.Model):
    board = models.ForeignKey(Board, on_delte=models.CASCADE)
    original_poster = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    likes = models.IntegerField()
    comment = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Badge(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    icon = models.FileField(upload_to="badges/")

class Event(models.Model):
    EPIC = "ep"
    RARE = "ra"
    COMMON = "co"
    DIFFICULTY_CHOICES = {
        EPIC: "epic",
        RARE: "rare",
        COMMON: "common"
    }
    name = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=2, choices=DIFFICULTY_CHOICES, default=COMMON)
    icon = models.FileField(upload_to="events/")

