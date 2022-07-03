import pytest
from rest_framework.test import APIClient

from users.models import User
from budgets.models import Budget

client = APIClient()


@pytest.fixture()
def budget_payload():
    """Common request payload for user creation tests"""
    return {
        "name": "test_budget",
    }


@pytest.fixture()
def create_budget(create_user, budget_payload):
    client.force_authenticate(create_user)
    client.post("/budgets/budgets/", data=budget_payload)
    budget = Budget.objects.get(name__exact=budget_payload["name"])
    yield budget
    Budget.objects.all().delete()


@pytest.fixture()
def create_budget_with_balance(create_user, create_budget, budget_payload):

    def generate_record(name, value, is_expense):
        return {
            "name": name,
            "value": value,
            "is_expense": is_expense,
            "budget": create_budget.pk
        }

    for i in range(4):
        client.force_authenticate(create_user)
        client.post("/budgets/records/", data=generate_record(f"income_{i}", i, False))
        client.post("/budgets/records/", data=generate_record(f"expense_{i}", 2 * i, True))

    return Budget.objects.get(name__exact=budget_payload["name"])


@pytest.fixture()
def create_and_share_budget(create_user, create_user_2, create_budget):
    client.force_authenticate(create_user)
    client.patch("/budgets/share/", data=dict(budget=create_budget.pk, user=create_user_2.username))

    return create_budget
