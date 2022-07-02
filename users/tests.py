# pylint: disable=missing-function-docstring
# Create your tests here.
import json

import pytest
from rest_framework.test import APIClient

from users.models import User

pytestmark = pytest.mark.django_db
client = APIClient()


def test_user_create(user_payload):
    response = client.post("/users/", data=user_payload)
    assert response.status_code == 201
    assert User.objects.filter(username__exact=user_payload["username"]).count() == 1


def test_user_delete(create_user):
    User.objects.get(username__exact=create_user.username).delete()
    assert User.objects.filter(username__exact=create_user.username).count() == 0


def test_user_create_short_password(user_payload):
    user_payload['password'] = "123"
    response = client.post("/users/", data=user_payload)
    content = json.loads(response.content)
    assert response.status_code == 400
    assert content["password"] == ['Ensure this field has at least 6 characters.']


def test_user_create_invalid_email(user_payload):
    user_payload['email'] = "test"
    response = client.post("/users/", data=user_payload)
    content = json.loads(response.content)
    assert response.status_code == 400
    assert content["email"] == ['Enter a valid email address.']


def test_user_create_duplicate_name(create_user, user_payload):
    user_payload['username'] = create_user.username
    response = client.post("/users/", data=user_payload)
    content = json.loads(response.content)
    assert response.status_code == 400
    assert content['username'] == ["A user with that username already exists."]


def test_user_create_duplicate_email(create_user, user_payload):
    user_payload['email'] = create_user.email
    response = client.post("/users/", data=user_payload)
    content = json.loads(response.content)
    assert response.status_code == 400
    assert content[0] == "This email is already used by different account"
