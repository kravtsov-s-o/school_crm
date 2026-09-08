from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from pricing.models import TeacherRate
from pricing.serializers.admin.teacher_rate import (
    TeacherRateAdminListSerializer,
    TeacherRateAdminSerializer,
)


@extend_schema(tags=["Admin: Teacher Rate"])
class TeacherRateAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for the Teacher Rate grid."""
    permission_classes = (IsAdminUser, DjangoModelPermissions)

    def get_serializer_class(self):
        if self.action == "list":
            return TeacherRateAdminListSerializer
        return TeacherRateAdminSerializer

    def get_queryset(self):
        qs = (TeacherRate.objects
              .select_related("currency", "language", "lesson_type", "grade"))
        if self.action != "list":
            qs = qs.prefetch_related("rows", "rows__duration")
        return qs

    filterset_fields = ("currency", "language", "lesson_type", "grade", "is_active")
    search_fields = ("name", "language__name", "lesson_type__name")
    ordering_fields = ("name", "language__name", "lesson_type__name", "grade__name", "is_active")
