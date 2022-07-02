from django.db import models

from users.models import User

# Create your models here.
class Budget(models.Model):

    name = models.CharField(blank=False, null=False, max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Record(models.Model):

    name = models.CharField(blank=False, null=False, max_length=150)
    value = models.FloatField(blank=False, null=False)
    is_expense = models.BooleanField(blank=True, null=False, default=False)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
