from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import views
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


class BusinessEndpoint(views.APIView):
    def get(self, request: Request) -> Response:
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")
        radius = request.query_params.get("radius")

        qs = None
        businesses = BusinessSerializer(qs, many=True)
        count = 0

        serializer = BusinessSerializer(
            {
                "location": {
                    "lat": lat,
                    "lon": lon,
                },
                count: count,
                "businesses": businesses.data,
            }
        )
        return Response(serializer.data)
