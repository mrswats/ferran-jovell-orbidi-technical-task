from typing import Any

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from orbidi.auth import models as auth_models
from orbidi.business import models


@pytest.fixture
def url():
    def _(url_name: str, **kwargs: Any):
        return reverse(url_name, kwargs=kwargs)

    return _


@pytest.fixture
def user():
    return auth_models.User.objects.create_user(
        username="foo",
        password="bar",
        email="foo@bar.com",
    )


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def business():
    return models.Business.objects.create(
        name="foo",
        iae_code="E471.1",
        rentability=50,
        typology=0.7,
        distance_to_the_city_center=100,
        latitude=41.473748,
        longitude=2.085348,
    )
