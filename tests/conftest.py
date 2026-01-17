import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from orbidi.auth import models


@pytest.fixture
def url():
    def _(*args, **kwargs):
        return reverse(*args, **kwargs)

    return _


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture
def user():
    return models.User.objects.create_user(
        username="foo",
        password="bar",
        email="foo@bar.com",
    )
