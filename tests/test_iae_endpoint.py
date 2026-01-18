from http import HTTPStatus
from typing import Any

import pytest
from rest_framework.test import APIClient

from orbidi.business import models


@pytest.fixture
def admin_client(user):
    user.is_staff = True
    user.save()

    client = APIClient()
    client.force_authenticate(user)

    return client


@pytest.fixture
def iae_data():
    return {
        "code": "E471.1",
        "description": "Pasta Papelera",
    }


@pytest.fixture
def iae():
    return models.IAE.objects.create(
        code="foo",
        description="code for foo",
    )


@pytest.fixture
def iae_url_list(url):
    return url("api:iae-list")


@pytest.fixture
def iae_url_detail(url):
    def _(iae_id: str) -> str:
        return url("api:iae-detail", pk=iae_id)

    return _


@pytest.fixture
def create_iae(admin_client, iae_url_list):
    def _(data: dict[str, Any]):
        return admin_client.post(iae_url_list, data=data)

    return _


@pytest.fixture
def retrieve_iae(admin_client, iae_url_detail):
    def _(iae_id: str):
        return admin_client.get(iae_url_detail(iae_id))

    return _


@pytest.fixture
def list_iae(admin_client, iae_url_list):
    def _():
        return admin_client.get(iae_url_list)

    return _


@pytest.fixture
def update_iae(admin_client, iae_url_detail):
    def _(iae_id: str, data: dict[str, Any]):
        return admin_client.patch(iae_url_detail(iae_id), data=data)

    return _


@pytest.fixture
def delete_iae(admin_client, iae_url_detail):
    def _(iae_id: str):
        return admin_client.delete(iae_url_detail(iae_id))

    return _


def test_iae_url_list(iae_url_list):
    assert iae_url_list == "/api/iae/"


def test_iae_url_detail(iae_url_detail):
    assert iae_url_detail("iae-id") == "/api/iae/iae-id/"


@pytest.mark.django_db
def test_iae_create_status_code(create_iae, iae_data):
    response = create_iae(data=iae_data)
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_iae_create_data(create_iae, iae_data):
    response = create_iae(data=iae_data)
    assert response.json() == iae_data


@pytest.mark.django_db
def test_iae_retrieve_status_code(retrieve_iae, iae):
    response = retrieve_iae(iae.pk)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_iae_retrieve_data(retrieve_iae, iae):
    response = retrieve_iae(iae.pk)
    assert response.json() == {"code": "foo", "description": "code for foo"}


@pytest.mark.django_db
def test_iae_list_status_code(list_iae):
    response = list_iae()
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_iae_list_data(list_iae, iae):
    response = list_iae()
    assert response.json()["results"] == [{"code": "foo", "description": "code for foo"}]


@pytest.mark.django_db
def test_iae_update_status_code(update_iae, iae):
    response = update_iae(iae.pk, {"description": "foo for description"})
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_iae_update_data(update_iae, iae):
    response = update_iae(iae.pk, {"description": "foo for description"})
    assert response.json() == {"code": "foo", "description": "foo for description"}


@pytest.mark.django_db
def test_iae_delete_status_code(delete_iae, iae):
    response = delete_iae(iae.pk)
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.django_db
def test_iae_delete_data(delete_iae, iae):
    response = delete_iae(iae.pk)
    assert response.content == b""
