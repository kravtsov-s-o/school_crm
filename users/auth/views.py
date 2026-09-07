from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.auth.serializers import PasswordResetConfirmSerializer, PasswordResetRequestSerializer

User = get_user_model()


@extend_schema(request=PasswordResetRequestSerializer, responses={200: None}, tags=["Auth"])
class PasswordResetRequestView(APIView):
    """Start a password reset — email a reset link to the address. Always returns
    200 and never reveals whether the email is registered (anti-enumeration)."""

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = (User.objects
                .filter(email=serializer.validated_data["email"], is_active=True)
                .first())
        if user is not None:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = f"{settings.FRONTEND_URL}/reset_password?uid={uid}&token={token}"
            send_mail("Password reset", f"Reset link: {link}", None, [user.email])
        return Response(status=status.HTTP_200_OK)


@extend_schema(request=PasswordResetConfirmSerializer, responses={200: None}, tags=["Auth"])
class PasswordResetConfirmView(APIView):
    """Complete a password reset — validate uid + token and set the new password."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data
        try:
            uid = force_str(urlsafe_base64_decode(d["uid"]))
            user = User.objects.get(pk=uid, is_active=True)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError({"uid": "Invalid reset link."}) from None

        if not default_token_generator.check_token(user, d["token"]):
            raise serializers.ValidationError({"token": "Invalid or expired reset link."})

        user.set_password(d["new_password"])
        user.save(update_fields=["password"])
        return Response(status=status.HTTP_200_OK)
