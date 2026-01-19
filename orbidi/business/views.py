from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos.point import Point
from rest_framework import permissions
from rest_framework import views
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from orbidi.business import models
from orbidi.business import serializers


class BusinessEndpoint(views.APIView):
    def get(self, request: Request) -> Response:
        latitude = float(request.query_params.get("lat", "0.0"))
        longitude = float(request.query_params.get("lon", "0.0"))
        radius = int(request.query_params.get("radius", "0"))

        qs = (
            models.Business.objects.annotate(
                distance=Distance(
                    Point(latitude, longitude, srid=4326),
                    "location",
                ),
            )
            .filter(distance__lt=radius)
            .order_by("conversion_rate")
        )

        serializer = serializers.BusinessesSerializer(
            {
                "location": {
                    "lat": latitude,
                    "lon": longitude,
                },
                "count": qs.count(),
                "businesses": qs,
            }
        )
        return Response(serializer.data)


class IAEEndpoint(viewsets.ModelViewSet):
    queryset = models.IAE.objects.all()
    serializer_class = serializers.IAESerializer
    permission_classes = (permissions.IsAdminUser,)
