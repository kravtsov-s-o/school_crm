from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import Coalesce
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from users.models import StudentProfile
from users.serializers.admin.student import (
    StudentAdminCreateSerializer,
    StudentAdminListSerializer,
    StudentAdminSerializer,
)


@extend_schema(tags=["Admin: Students"])
class StudentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """Admin management of students — create/list/retrieve/update the whole person
    (User account + StudentProfile) in one form. No delete: deactivate via the
    ``is_student`` flag / ``is_active``."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    queryset = (StudentProfile.objects
                .select_related("user", "teacher__user", "currency", "company", "account")
                .prefetch_related("languages", "personal_plans")
                .annotate(balance=Coalesce(Sum("account__transactions__amount"), Decimal(0)))
                .order_by("user__first_name", "user__last_name")
                .distinct())
    filterset_fields = ("teacher", "currency", "company",
                        "languages", "personal_plans", "is_active")
    search_fields = ("user__first_name", "user__last_name", "user__email", "user__username")
    ordering_fields = ("user__first_name", "user__last_name", "is_active", "balance")

    def get_serializer_class(self):
        if self.action == "create":
            return StudentAdminCreateSerializer
        elif self.action == "list":
            return StudentAdminListSerializer
        else:
            return StudentAdminSerializer
