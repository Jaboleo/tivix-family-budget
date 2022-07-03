from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import Budget, Record
from users.serializers import UserSerializer


class RecordSerializer(serializers.ModelSerializer):

    value = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Record
        fields = ("id", "name", "value", "date_created", "date_updated", "is_expense")


class BudgetSerializer(serializers.ModelSerializer):

    owner = UserSerializer(read_only=True)
    shared_with = UserSerializer(many=True, read_only=True, required=False)
    balance = serializers.SerializerMethodField(read_only=True)
    incomes = serializers.SerializerMethodField(read_only=True)
    expenses = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Budget
        fields = ("id", "name", "owner", "balance", "incomes", "expenses", "shared_with")

    def get_incomes(self, obj):
        incomes = obj.record_set.filter(is_expense=False)
        return RecordSerializer(incomes, many=True).data

    def get_expenses(self, obj):
        expenses = obj.record_set.filter(is_expense=True)
        return RecordSerializer(expenses, many=True).data

    def get_balance(self, obj):
        incomes = obj.record_set.filter(is_expense=False)
        expenses = obj.record_set.filter(is_expense=True)
        return sum(record.value for record in incomes) - sum(record.value for record in expenses)
