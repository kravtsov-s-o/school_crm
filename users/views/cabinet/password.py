from django.contrib.auth import update_session_auth_hash
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers.cabinet.password import ChangePasswordSerializer


@extend_schema(tags=["Cabinet"], request=ChangePasswordSerializer, responses={200: None})
class ChangePasswordView(APIView):
    """Change the signed-in user's password (requires the current password)."""

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data,
                                              context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        update_session_auth_hash(request, user)
        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
