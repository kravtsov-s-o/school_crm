from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import Coalesce
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from users.models import TeacherProfile
from users.serializers.admin.teacher import (
    TeacherAdminCreateSerializer,
    TeacherAdminListSerializer,
    TeacherAdminSerializer,
)


@extend_schema(tags=["Admin: Teachers"])
class TeacherViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """Admin management of teachers — create/list/retrieve/update the whole person
    (User account + TeacherProfile) in one form. No delete: deactivate via the
    ``is_teacher`` flag / ``is_active``."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    queryset = (TeacherProfile.objects
                .select_related("user", "currency", "account", "grade")
                .prefetch_related("languages", "lesson_types")
                .annotate(balance=Coalesce(Sum("account__transactions__amount"), Decimal(0)))
                .order_by("user__first_name", "user__last_name")
                .distinct())
    filterset_fields = ("currency", "grade", "languages", "lesson_types", "is_active")
    search_fields = ("user__first_name", "user__last_name", "user__email", "user__username")
    ordering_fields = ("user__first_name", "user__last_name", "is_active", "balance")

    def get_serializer_class(self):
        if self.action == "create":
            return TeacherAdminCreateSerializer
        elif self.action == "list":
            return TeacherAdminListSerializer
        else:
            return TeacherAdminSerializer
