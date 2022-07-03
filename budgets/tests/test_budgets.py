# pylint: disable=missing-function-docstring
# Create your tests here.
import json

import pytest
from rest_framework.test import APIClient

from users.models import User
from budgets.models import Budget

pytestmark = pytest.mark.django_db
client = APIClient()


def test_budget_create(create_user, budget_payload):
    client.force_authenticate(create_user)
    response = client.post("/budgets/budgets/", data=budget_payload)
    assert response.status_code == 201
    assert Budget.objects.filter(name__exact=budget_payload["name"]).count() == 1


def test_budget_patch(create_user, create_budget):
    client.force_authenticate(create_user)
    client.patch(f"/budgets/budgets/{create_budget.pk}/", data={"name": "new_name"})
    assert Budget.objects.filter(name="teast_name").count() == 0
    assert Budget.objects.filter(name="new_name").count() == 1


def test_budget_delete(create_user, create_budget):
    client.force_authenticate(create_user)
    response = client.delete(f"/budgets/budgets/{create_budget.pk}/")
    assert response.status_code == 204
    assert Budget.objects.filter(pk=create_budget.pk).count() == 0


def test_budget_get_one(create_user, create_budget):
    client.force_authenticate(create_user)
    response = client.get(f"/budgets/budgets/{create_budget.pk}/")
    content = json.loads(response.content)
    assert response.status_code == 200
    assert isinstance(content, dict)


def test_budget_list(create_user, create_budget):
    client.force_authenticate(create_user)
    response = client.get("/budgets/budgets/")
    content = json.loads(response.content)
    assert response.status_code == 200
    assert len(content) == 1


def test_budget_list_no_owned_budgets(create_user, create_budget, create_user_2):
    client.force_authenticate(create_user_2)
    response = client.get("/budgets/budgets/")
    content = json.loads(response.content)
    assert response.status_code == 200
    assert len(content) == 0


def test_budget_calculate_balance(create_user, create_budget_with_balance):
    client.force_authenticate(create_user)
    response = client.get(f"/budgets/budgets/{create_budget_with_balance.pk}/")
    content = json.loads(response.content)
    assert response.status_code == 200
    assert content["balance"] == float(-6)


def test_budget_share(create_user, create_budget, create_user_2):
    client.force_authenticate(create_user)
    response = client.patch("/budgets/share/", data=dict(budget=create_budget.pk, user=create_user_2.username))
    client.logout()
    client.force_authenticate(create_user_2)
    response = client.get("/budgets/shared-with-me/")
    content = json.loads(response.content)
    assert response.status_code == 200
    assert len(content) == 1


def test_budget_share_with_owner(create_user, create_budget):
    client.force_authenticate(create_user)
    response = client.patch("/budgets/share/", data=dict(budget=create_budget.pk, user=create_user.username))
    content = json.loads(response.content)
    assert response.status_code == 403
    assert content == 'Cannot share with yourself'


def test_budget_share_not_budget_owner(create_budget, create_user_2):
    client.force_authenticate(create_user_2)
    response = client.patch("/budgets/share/", data=dict(budget=create_budget.pk, user=create_user_2.username))
    content = json.loads(response.content)
    assert response.status_code == 403
    assert content == "Cannot share other users' budgets"


def test_budget_unshare(create_user, create_user_2, create_and_share_budget):
    client.force_authenticate(create_user)
    response = client.patch("/budgets/unshare/", data=dict(budget=create_and_share_budget.pk,
                                                           user=create_user_2.username))
    client.logout()
    client.force_authenticate(create_user_2)
    response = client.get("/budgets/shared-with-me/")
    content = json.loads(response.content)
    assert response.status_code == 200
    assert len(content) == 0


def test_budget_list_shared_with_user(create_user_2, create_and_share_budget):
    client.force_authenticate(create_user_2)
    response = client.get("/budgets/shared-with-me/")
    content = json.loads(response.content)
    assert response.status_code == 200
    assert len(content) == 1
