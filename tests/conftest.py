from typing import Any

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from orbidi.auth import models


@pytest.fixture
def url():
    def _(url_name: str, **kwargs: Any):
        return reverse(url_name, kwargs=kwargs)

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
