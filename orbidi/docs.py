from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView


urlpatterns = [
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="docs-schema"),
        name="docs-html",
    ),
    path(
        "openapi.yaml",
        SpectacularAPIView.as_view(),
        name="docs-schema",
    ),
]
