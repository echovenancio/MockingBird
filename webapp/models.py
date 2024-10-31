from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import Group
   
Group.objects.create(name="verified_group")

class VerificationTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6)
