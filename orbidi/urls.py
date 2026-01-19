from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("orbidi.auth.urls", namespace="auth")),
    path("api/", include("orbidi.business.urls", namespace="api")),
    path("", include("orbidi.health.urls")),
    path("docs/", include("orbidi.docs")),
]
