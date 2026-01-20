from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos.point import Point
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiTypes
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from orbidi.business import models
from orbidi.business import serializers

parameter_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            "lat",
            OpenApiTypes.FLOAT,
            description="Latitude as a float",
        ),
        OpenApiParameter(
            "lon1",
            OpenApiTypes.FLOAT,
            description="Longitude as a float",
        ),
        OpenApiParameter(
            "radius",
            OpenApiTypes.INT,
            description="Radius of action in meters",
        ),
    ],
)


@parameter_schema
class BusinessEndpoint(viewsets.GenericViewSet):
    queryset = models.Business.objects.all()
    serializer_class = serializers.BusinessesSerializer
    pagination_class = None

    def list(self, request: Request) -> Response:
        latitude = float(self.request.query_params.get("lat", "0.0"))
        longitude = float(self.request.query_params.get("lon", "0.0"))
        radius = int(self.request.query_params.get("radius", "0"))

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

        serializer = self.get_serializer(
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


@parameter_schema
class CompetitorsEndpoint(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Business.objects.all()
    serializer_class = serializers.BusinessSerializer

    def get_business(self):
        return get_object_or_404(
            models.Business.objects.prefetch_related("iae"),
            external_id=self.kwargs["business_id"],
        )

    def get_queryset(self):
        latitude = float(self.request.query_params.get("lat", "0.0"))
        longitude = float(self.request.query_params.get("lon", "0.0"))
        radius = int(self.request.query_params.get("radius", "0"))

        business = self.get_business()

        return (
            models.Business.objects.exclude(pk=business.pk)
            .filter(iae__code__startswith=f"{business.iae.code[0]}")
            .annotate(
                distance=Distance(
                    Point(latitude, longitude, srid=4326),
                    "location",
                ),
            )
            .filter(distance__lt=radius)
        )


class IAEEndpoint(viewsets.ModelViewSet):
    queryset = models.IAE.objects.all()
    serializer_class = serializers.IAESerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == "create":
            return serializers.IAECreateSerializer

        return super().get_serializer_class()
