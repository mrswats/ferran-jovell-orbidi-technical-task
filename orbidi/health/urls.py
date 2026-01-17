from django.urls import path

from orbidi.health import views

urlpatterns = [
    path("_health/", views.HealthEndpoint.as_view(), name="health"),
]
