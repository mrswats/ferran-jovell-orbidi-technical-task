from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos.point import Point
from django.core import validators
from django.db import models
from django.db.models import F
from django.db.models import Value
from django.db.models.functions import Concat

from orbidi.business import metrics


class IAE(models.Model):
    code = models.CharField()
    description = models.TextField()


class Business(models.Model):
    external_id = models.GeneratedField(
        expression=Concat(Value("BIZ-"), F("id")),
        output_field=models.CharField(),
        db_persist=True,
    )
    name = models.CharField()
    iae_code = models.CharField()
    rentability = models.IntegerField()
    typology = models.FloatField(
        validators=[
            validators.MaxValueValidator(1.0),
            validators.MinValueValidator(0.0),
        ]
    )
    distance_to_the_city_center = models.IntegerField()
    conversion_rate = models.FloatField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = geo_models.PointField(blank=True)

    def save(self, *args, **kwargs):
        self.location = Point(self.latitude, self.longitude)
        self.conversion_rate = metrics.conversion_rate_probability(
            self.rentability,
            self.typology,
            self.distance_to_the_city_center,
        )

        return super().save(*args, **kwargs)

    @property
    def coordinates(self) -> dict[str, float]:
        return {
            "lat": self.latitude,
            "lon": self.longitude,
        }
