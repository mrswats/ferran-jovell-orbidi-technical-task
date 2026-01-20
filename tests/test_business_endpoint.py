from http import HTTPStatus
from typing import Any

import pytest


@pytest.fixture
def business_url(url):
    return url("api:business-list")


@pytest.fixture
def business_list(client, business_url):
    def _(data: dict[str, Any]):
        return client.get(business_url, data=data)

    return _


def test_business_url(business_url):
    assert business_url == "/api/business/"


@pytest.mark.django_db
def test_business_str(business):
    assert str(business) == "foo"


@pytest.mark.django_db
def test_business_endpoint_status_code(business_list):
    response = business_list({"lat": 41.473748, "lon": 2.085348, "radius": 5000})
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_business_endpoint_empty_data(business_list):
    response = business_list({"lat": 41.473748, "lon": 2.085348, "radius": 5000})
    assert response.json() == {
        "businesses": [],
        "count": 0,
        "location": {
            "lat": 41.473748,
            "lon": 2.085348,
        },
    }


@pytest.mark.django_db
def test_business_endpoint_non_empty_data(business_list, business):
    response = business_list({"lat": 41.50, "lon": 2.085348, "radius": 5000})
    assert response.json() == {
        "businesses": [
            {
                "coordinates": {
                    "lat": 41.473748,
                    "lon": 2.085348,
                },
                "external_id": "BIZ-1",
                "iae_code": "471.1",
                "name": "foo",
                "rentability": 50,
            },
        ],
        "count": 1,
        "location": {
            "lat": 41.50,
            "lon": 2.085348,
        },
    }


@pytest.mark.django_db
def test_business_endpoint_outside_of_radius_data(business_list, business):
    response = business_list({"lat": 41.50, "lon": 2.085348, "radius": 1000})
    assert response.json() == {
        "businesses": [],
        "count": 0,
        "location": {
            "lat": 41.50,
            "lon": 2.085348,
        },
    }
