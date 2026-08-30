from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser
from rest_framework.response import Response

from users.models import User
from users.serializers.admin.user import (
    UserAdminCreateSerializer,
    UserAdminSerializer,
    UserAdminSetPasswordSerializer,
)


@extend_schema(tags=["Admin: Users"])
class UserAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for ``User`` accounts. Gated by ``IsAdminUser`` +
    ``DjangoModelPermissions`` (per-model rights granted via groups). DELETE
    soft-deletes the user (``is_active=False``); ``create`` accepts a password,
    other actions do not — password changes go through :meth:`set_password`."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    queryset = (User.objects.all()
                .prefetch_related("groups", "user_permissions")
                .order_by("-is_active", "first_name", "last_name"))
    filterset_fields = ("is_active", "is_staff", "is_superuser", "is_student", "is_teacher")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering_fields = ("first_name", "last_name", "email", "username", "is_active")

    def get_serializer_class(self):
        if self.action == "create":
            return UserAdminCreateSerializer
        return UserAdminSerializer

    @extend_schema(request=UserAdminSetPasswordSerializer,
                   responses={200: None})
    @action(detail=True, methods=["post"], url_path="set-password",
            permission_classes=[IsAdminUser])
    def set_password(self, request, pk=None):
        """Set a new password for the target user (admin reset — no old password
        required). Bypasses ``DjangoModelPermissions`` (``IsAdminUser`` only), as
        a POST here would otherwise map to the ``add`` right, not ``change``."""
        user = self.get_object()

        serializer = UserAdminSetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data["password"])
        user.save(update_fields=["password"])

        return Response(
            {"detail": "Password has been reset."}, status=status.HTTP_200_OK
        )
