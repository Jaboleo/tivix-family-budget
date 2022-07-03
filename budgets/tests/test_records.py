# pylint: disable=missing-function-docstring
# Create your tests here.
import json

import pytest
from rest_framework.test import APIClient

from users.models import User
from budgets.models import Record
from budgets.serializers import BudgetSerializer

pytestmark = pytest.mark.django_db
client = APIClient()


def test_record_delete(create_user, create_budget_with_balance):
    client.force_authenticate(create_user)
    response = client.delete("/budgets/records/1/")
    content = json.loads(response.content)
    assert response.status_code == 200
    assert content == "Record 1 deleted"


def test_record_list(create_user, create_budget_with_balance):
    client.force_authenticate(create_user)
    response = client.get("/budgets/records/")
    content = json.loads(response.content)
    assert response.status_code == 403
    assert content == "Cannot list incomes/expenses outside budgets"
