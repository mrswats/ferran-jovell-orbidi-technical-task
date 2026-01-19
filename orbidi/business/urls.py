from django.urls import path
from django.urls import re_path
from rest_framework import routers

from orbidi.business import views

router = routers.SimpleRouter()
router.register("iae", views.IAEEndpoint, basename="iae")

urlpatterns = [
    path(
        "business/",
        views.BusinessEndpoint.as_view(),
        name="business",
    ),
    re_path(
        "competitors/(?P<business_id>[^/]+?)/",
        views.CompetitorsEndpoint.as_view(),
        name="competitors",
    ),
    *router.urls,
]

app_name = "api"
