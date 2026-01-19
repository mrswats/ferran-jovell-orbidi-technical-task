from rest_framework import routers

from orbidi.business import views

router = routers.SimpleRouter()
router.register(
    "iae",
    views.IAEEndpoint,
    basename="iae",
)
router.register(
    "business",
    views.BusinessEndpoint,
    basename="business",
)
router.register(
    "competitors/(?P<business_id>[^/]+?)",
    views.CompetitorsEndpoint,
    basename="competitors",
)

urlpatterns = router.urls

app_name = "api"
