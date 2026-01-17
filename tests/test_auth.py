from http import HTTPStatus

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken

from orbidi.auth import models


@pytest.fixture
def unauthenticated_client():
    return APIClient()


@pytest.fixture
def token_url(url):
    return url("auth:token-pair")


@pytest.fixture
def refresh_token_url(url):
    return url("auth:token-refresh")


@pytest.fixture
def access_token():
    def _(user: models.User) -> str:
        return str(AccessToken.for_user(user))

    return _


@pytest.fixture
def get_token(unauthenticated_client, token_url):
    def _(data: dict[str, str]):
        return unauthenticated_client.post(token_url, data=data)

    return _


@pytest.fixture
def refresh_token(unauthenticated_client, refresh_token_url):
    def _(token: str):
        return unauthenticated_client.post(refresh_token_url, data={"refresh": token})

    return _


@pytest.fixture
def verify_token(unauthenticated_client, verify_token_url):
    def _(token: str):
        return unauthenticated_client.post(verify_token_url, data={"token": token})

    return _


def test_auth_url(token_url):
    assert token_url == "/auth/token/"


def test_refresh_url(refresh_token_url):
    assert refresh_token_url == "/auth/refresh/"


@pytest.mark.django_db
def test_get_token_status_code(get_token, user):
    response = get_token(
        {
            "username": user.username,
            "password": "bar",
        },
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_get_token_data(get_token, user):
    response = get_token(
        {
            "username": user.username,
            "password": "bar",
        },
    )
    assert set(response.json().keys()) == {"refresh", "access"}


@pytest.mark.django_db
def test_refresh_token_status_code(refresh_token, user):
    token = RefreshToken.for_user(user)
    response = refresh_token(f"{token}")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_refresh_token_data(refresh_token, user):
    token = RefreshToken.for_user(user)
    response = refresh_token(f"{token}")
    assert set(response.json().keys()) == {"access"}
