from django.urls import path
from rest_framework import routers

from orbidi.business import views

router = routers.SimpleRouter()
router.register("iae", views.IAEEndpoint, basename="iae")

urlpatterns = [
    path("business/", views.BusinessEndpoint.as_view(), name="business"),
    *router.urls,
]

app_name = "api"
