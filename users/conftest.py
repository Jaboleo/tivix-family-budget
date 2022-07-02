import pytest
from rest_framework.test import APIClient

from users.models import User

client = APIClient()


@pytest.fixture()
def user_payload():
    """Common request payload for user creation tests"""
    return {
        "username": "test1",
        "email": "test1@test.com",
        "password": "123456"
    }


@pytest.fixture()
def create_user():
    """Create a user to use later in tests"""
    payload = {
        "username": "fixture_user1",
        "email": "fixture@test.com",
        "password": "123456"
    }
    client.post("/users/", data=payload)

    yield User.objects.get(username__exact=payload['username'])
