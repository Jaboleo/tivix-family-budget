"""Register your models here."""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    email = models.EmailField(unique=True, blank=False)

    def __str__(self):
        return str(self.username)
