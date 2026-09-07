from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from users.auth.views import PasswordResetConfirmView, PasswordResetRequestView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='jwt-login'),
    path('refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path("logout/", TokenBlacklistView.as_view(), name="jwt-logout"),
    path("password-reset/", PasswordResetRequestView.as_view()),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view()),
]
