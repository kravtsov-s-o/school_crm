from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions

from pricing.models import SchoolPrice, TeacherRate, PersonalPlan
from pricing.serializers.admin.price import SchoolPriceAdminSerializer, TeacherRateAdminSerializer, \
    PersonalPlanAdminSerializer


@extend_schema(tags=["Admin: School Price"])
class SchoolPriceAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for the school base price grid."""
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = SchoolPriceAdminSerializer
    queryset = (SchoolPrice.objects
                .select_related("currency", "language", "lesson_type")
                .prefetch_related("rows", "rows__duration"))


@extend_schema(tags=["Admin: Teacher Rate"])
class TeacherRateAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for the Teacher Rate grid."""
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = TeacherRateAdminSerializer
    queryset = (TeacherRate.objects
                .select_related("currency", "language", "lesson_type", "grade")
                .prefetch_related("rows", "rows__duration"))


@extend_schema(tags=["Admin: Personal Plan"])
class PersonalPlanAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for the Personal Plan grid."""
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = PersonalPlanAdminSerializer
    queryset = (PersonalPlan.objects
                .select_related("currency", "language", "lesson_type")
                .prefetch_related("rows", "rows__duration"))