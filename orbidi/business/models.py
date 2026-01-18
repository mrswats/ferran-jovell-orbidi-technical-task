from django.core import validators
from django.db import models
from django.db.models import F
from django.db.models.functions import Concat


class IAE(models.Model):
    code = models.CharField()
    description = models.TextField()


class Business(models.Model):
    external_id = models.GeneratedField(
        expression=Concat(F("id"), F("id")),
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
    latitude = models.FloatField()
    longitude = models.FloatField()

    @property
    def coordinates(self) -> dict[str, float]:
        return {
            "lat": self.latitude,
            "lon": self.longitude,
        }
