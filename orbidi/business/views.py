from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos.point import Point
from rest_framework import permissions
from rest_framework import views
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
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


class CompetitorsEndpoint(views.APIView):
    def get_object(self):
        return get_object_or_404(models.Business, external_id=self.kwargs["business_id"])

    def get(self, request: Request, business_id: str) -> Response:
        latitude = float(request.query_params.get("lat", "0.0"))
        longitude = float(request.query_params.get("lon", "0.0"))
        radius = int(request.query_params.get("radius", "0"))

        business = self.get_object()

        qs = (
            models.Business.objects.exclude(pk=business.pk)
            .filter(iae_code__startswith=f"{business.iae_code[:1]}")
            .annotate(
                distance=Distance(
                    Point(latitude, longitude, srid=4326),
                    "location",
                ),
            )
            .filter(distance__lt=radius)
        )

        serializer = serializers.BusinessSerializer(qs, many=True)
        return Response(serializer.data)


class IAEEndpoint(viewsets.ModelViewSet):
    queryset = models.IAE.objects.all()
    serializer_class = serializers.IAESerializer
    permission_classes = (permissions.IsAdminUser,)
