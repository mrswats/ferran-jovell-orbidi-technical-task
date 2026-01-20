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
def iae_471():
    return models.IAE.objects.create(
        code="471.1",
        group="E",
        value=500,
        description="Pasta Papelera",
    )


@pytest.fixture
def iae_453():
    return models.IAE.objects.create(
        code="453",
        group="E",
        value=649,
        description="Confeccion prendas de vestir.",
    )


@pytest.fixture
def business(iae_471):
    return models.Business.objects.create(
        name="foo",
        iae=iae_471,
        rentability=50,
        distance_to_the_city_center=100,
        latitude=41.473748,
        longitude=2.085348,
    )


@pytest.fixture
def competitor(iae_453):
    return models.Business.objects.create(
        name="bar",
        iae=iae_453,
        rentability=80,
        distance_to_the_city_center=250,
        latitude=41.409188,
        longitude=2.074123,
    )
