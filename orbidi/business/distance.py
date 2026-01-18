from geopy.distance import geodesic


def dist(orig: tuple[float, float], dest: tuple[float, float]) -> float:
    return geodesic(orig, dest).meters
