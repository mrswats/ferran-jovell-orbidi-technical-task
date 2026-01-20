from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos.point import Point
from django.db import models
from django.db.models import F
from django.db.models import Value
from django.db.models.functions import Concat

from orbidi.business import metrics


class IAE(models.Model):
    code = models.CharField()
    group = models.CharField()
    value = models.IntegerField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.code


class Business(models.Model):
    external_id = models.GeneratedField(
        expression=Concat(Value("BIZ-"), F("id")),
        output_field=models.CharField(),
        db_persist=True,
    )
    name = models.CharField()
    iae = models.ForeignKey(IAE, on_delete=models.DO_NOTHING, related_name="businesses")
    rentability = models.IntegerField()
    distance_to_the_city_center = models.IntegerField()
    conversion_rate = models.FloatField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = geo_models.PointField(blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.location = Point(self.latitude, self.longitude)
        self.conversion_rate = metrics.conversion_rate_probability(
            self.rentability,
            self.iae.value,
            self.distance_to_the_city_center,
        )

        return super().save(*args, **kwargs)

    @property
    def coordinates(self) -> dict[str, float]:
        return {
            "lat": self.latitude,
            "lon": self.longitude,
        }
