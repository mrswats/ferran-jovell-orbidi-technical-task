from math import exp

RENTABILITY_FACTOR = 0.2
TYPOLOGY_FACTOR = 0.4
PROXIMITY_FACTOR = 0.4


def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))


def rentability_normalization(rentability: float) -> float:
    return rentability / 100


def proximity_normalization(distance: float) -> float:
    return 1 / (1 + distance)


def conversion_rate_probability(
    rentability: int,
    typoloy: float,
    distance: float,
) -> float:
    arg = (
        RENTABILITY_FACTOR * rentability_normalization(rentability)
        + TYPOLOGY_FACTOR * typoloy
        + PROXIMITY_FACTOR * proximity_normalization(distance)
    )

    return sigmoid(arg)
