from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenBlacklistView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='jwt-login'),
    path('refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path("logout/", TokenBlacklistView.as_view(), name="jwt-logout"),
]
