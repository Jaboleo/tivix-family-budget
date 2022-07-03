from django.db import models

from users.models import User


# Create your models here.
class Budget(models.Model):

    name = models.CharField(blank=False, null=False, max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    shared_with = models.ManyToManyField(User, blank=True, related_name="shared_budgets")


class Record(models.Model):

    name = models.CharField(blank=False, null=False, max_length=150)
    value = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=10)
    is_expense = models.BooleanField(blank=False, null=False, default=False)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
