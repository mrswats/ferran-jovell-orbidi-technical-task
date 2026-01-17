from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("orbidi.auth.urls", namespace="auth")),
    path("", include("orbidi.health.urls")),
]
