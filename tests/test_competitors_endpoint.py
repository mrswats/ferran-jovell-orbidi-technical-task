from http import HTTPStatus
from typing import Any

import pytest


@pytest.fixture
def competitors_url(url):
    def _(business_id: str) -> str:
        return url("api:competitors-list", business_id=business_id)

    return _


@pytest.fixture
def list_competitors(client, competitors_url):
    def _(business_id: str, data: dict[str, Any]):
        return client.get(competitors_url(business_id), data=data)

    return _


def test_competitors_url(competitors_url):
    assert competitors_url("business-id") == "/api/competitors/business-id/"


@pytest.mark.django_db
def test_competitors_endpoint_status_code(list_competitors, business):
    response = list_competitors(business.external_id, {})
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_competitors_endpoint_business_not_found_status_code(list_competitors):
    response = list_competitors("foo", {})
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_competitors_endpoint_no_params_business_data(list_competitors, business):
    response = list_competitors(business.external_id, {})
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }


@pytest.mark.django_db
def test_competitors_endpoint_business_data(list_competitors, business, competitor):
    response = list_competitors(
        business.external_id, {"lat": 41.50, "lon": 2.085348, "radius": 20000}
    )
    assert response.json()["results"] == [
        {
            "coordinates": {
                "lat": 41.409188,
                "lon": 2.074123,
            },
            "external_id": "BIZ-2",
            "iae_code": "453",
            "name": "bar",
            "rentability": 80,
        },
    ]
