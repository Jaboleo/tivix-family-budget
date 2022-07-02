"""Register your models here."""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    name = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return str(self.name)
