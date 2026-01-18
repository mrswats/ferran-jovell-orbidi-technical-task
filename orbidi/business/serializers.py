from rest_framework import serializers

from orbidi.business import models


class BusinessSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="external_id")

    class Meta:
        model = models.Business
        fields = (
            "id",
            "name",
            "iae_code",
            "rentability",
            "coordinates",
        )


class BusinessesSerializer(serializers.Serializer):
    location = serializers.DictField()
    count = serializers.IntegerField()
    businesses = BusinessSerializer(many=True)
