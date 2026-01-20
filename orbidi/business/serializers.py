from rest_framework import serializers

from orbidi.business import models


class BusinessSerializer(serializers.ModelSerializer):
    iae_code = serializers.CharField(source="iae.code")

    class Meta:
        model = models.Business
        fields = (
            "external_id",
            "name",
            "iae_code",
            "rentability",
            "coordinates",
        )


class BusinessesSerializer(serializers.Serializer):
    location = serializers.DictField()
    count = serializers.IntegerField()
    businesses = BusinessSerializer(many=True)


class IAECreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IAE
        fields = (
            "code",
            "description",
            "group",
            "value",
        )


class IAESerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IAE
        fields = (
            "code",
            "description",
            "group",
            "value",
        )
        read_only_fields = (
            "code",
            "group",
        )
