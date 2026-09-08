from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from pricing.models import PersonalPlan
from pricing.serializers.admin.personal_plan import (
    PersonalPlanAdminListSerializer,
    PersonalPlanAdminSerializer,
)


@extend_schema(tags=["Admin: Personal Plan"])
class PersonalPlanAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for the Personal Plan grid."""
    permission_classes = (IsAdminUser, DjangoModelPermissions)

    def get_serializer_class(self):
        if self.action == "list":
            return PersonalPlanAdminListSerializer
        return PersonalPlanAdminSerializer

    def get_queryset(self):
        qs = PersonalPlan.objects.select_related("currency", "language", "lesson_type")
        if self.action != "list":
            qs = qs.prefetch_related("rows", "rows__duration")
        return qs

    filterset_fields = ("currency", "language", "lesson_type", "is_active")
    search_fields = ("name", "language__name", "lesson_type__name")
    ordering_fields = ("name", "language__name", "lesson_type__name", "is_active")
