from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from pricing.models import PersonalPlan, SchoolPrice, TeacherRate
from pricing.serializers.admin.price import (
    PersonalPlanAdminSerializer,
    SchoolPriceAdminSerializer,
    TeacherRateAdminSerializer,
)


@extend_schema(tags=["Admin: School Price"])
class SchoolPriceAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for the school base price grid."""
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = SchoolPriceAdminSerializer
    queryset = (SchoolPrice.objects
                .select_related("currency", "language", "lesson_type")
                .prefetch_related("rows", "rows__duration"))
    filterset_fields = ("currency", "language", "lesson_type", "is_active")
    search_fields = ("name", "language__name", "lesson_type__name")
    ordering_fields = ("name", "language__name", "lesson_type__name", "is_active")


@extend_schema(tags=["Admin: Teacher Rate"])
class TeacherRateAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for the Teacher Rate grid."""
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = TeacherRateAdminSerializer
    queryset = (TeacherRate.objects
                .select_related("currency", "language", "lesson_type", "grade")
                .prefetch_related("rows", "rows__duration"))
    filterset_fields = ("currency", "language", "lesson_type", "grade", "is_active")
    search_fields = ("name", "language__name", "lesson_type__name")
    ordering_fields = ("name", "language__name", "lesson_type__name", "grade__name", "is_active")


@extend_schema(tags=["Admin: Personal Plan"])
class PersonalPlanAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for the Personal Plan grid."""
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = PersonalPlanAdminSerializer
    queryset = (PersonalPlan.objects
                .select_related("currency", "language", "lesson_type")
                .prefetch_related("rows", "rows__duration"))
    filterset_fields = ("currency", "language", "lesson_type", "is_active")
    search_fields = ("name", "language__name", "lesson_type__name")
    ordering_fields = ("name", "language__name", "lesson_type__name", "is_active")
