from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
   
class VerificationTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6)
