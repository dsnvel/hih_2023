from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(default='user', max_length=64)
