from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token-pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]

app_name = "auth"
