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
