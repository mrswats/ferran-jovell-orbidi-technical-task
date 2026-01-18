from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response

from orbidi.business import serializers


class BusinessEndpoint(views.APIView):
    def get(self, request: Request) -> Response:
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")
        _radius = request.query_params.get("radius")

        qs = None
        businesses = serializers.BusinessSerializer(qs, many=True)
        count = 0

        serializer = serializers.BusinessSerializer(
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
