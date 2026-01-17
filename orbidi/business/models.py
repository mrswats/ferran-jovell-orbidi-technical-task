from django.db import models
from django.db.models import F
from django.db.models.function import Concat
from django.db.models.function import Cast


class IAE(models.Model):
    code = models.CharField()
    value = models.CharField()
    description = models.TextField()


class Business(models.Model):
    external_id = models.GeneratedField(
        Concat(
            "BIZ-",
            Cast(F("id")),
        ),
        output_field=models.CharField(),
        db_persist=True,
    )
    name = models.CharField()
    iae = models.ForeignKey(
        IAE,
        on_delete=models.DO_NOTHING,
        related_name="businesses",
    )
    rentability = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    @property
    def iae_code(self):
        return self.iae.code

    @property
    def coordinates(self) -> dict[str, float]:
        return {
            "lat": self.latitude,
            "lon": self.longitude,
        }
