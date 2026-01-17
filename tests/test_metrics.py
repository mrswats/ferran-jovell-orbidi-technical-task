import random

import pytest

from orbidi import metrics


@pytest.mark.parametrize(
    "arg, val",
    [(-100, 0.0), (100, 1.0), (0, 0.5)],
)
def test_sigmoid(arg, val):
    assert round(metrics.sigmoid(arg), 2) == val


def test_rentability():
    rentability = int(100 * random.random())

    assert metrics.rentability_normalization(rentability) <= 1.0


def test_proximity():
    distance = 100
    assert metrics.proximity_normalization(distance) == 1 / (1 + distance)


def test_conversion_rate_probability():
    assert metrics.conversion_rate_probability(50, 0.7, 100) == 0.5948279460681152
