from math import exp

RENTABILITY_FACTOR = 0.2
TYPOLOGY_FACTOR = 0.4
PROXIMITY_FACTOR = 0.4


def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))


def typoloy_normalization(typoloy: int) -> float:
    return typoloy / 1000


def rentability_normalization(rentability: float) -> float:
    return rentability / 100


def proximity_normalization(distance: float) -> float:
    return 1 / (1 + distance)


def conversion_rate_probability(
    rentability: int,
    typoloy: int,
    distance: float,
) -> float:
    arg = (
        RENTABILITY_FACTOR * rentability_normalization(rentability)
        + TYPOLOGY_FACTOR * typoloy_normalization(typoloy)
        + PROXIMITY_FACTOR * proximity_normalization(distance)
    )

    return sigmoid(arg)
