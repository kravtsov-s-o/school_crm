from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from pricing.models import SchoolPrice
from pricing.serializers.admin.school_price import (
    SchoolPriceAdminListSerializer,
    SchoolPriceAdminSerializer,
)


@extend_schema(tags=["Admin: School Price"])
class SchoolPriceAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for the school base price grid."""
    permission_classes = (IsAdminUser, DjangoModelPermissions)

    def get_serializer_class(self):
        if self.action == "list":
            return SchoolPriceAdminListSerializer
        return SchoolPriceAdminSerializer

    def get_queryset(self):
        qs = SchoolPrice.objects.select_related("currency", "language", "lesson_type")
        if self.action != "list":
            qs = qs.prefetch_related("rows", "rows__duration")
        return qs

    filterset_fields = ("currency", "language", "lesson_type", "is_active")
    search_fields = ("name", "language__name", "lesson_type__name")
    ordering_fields = ("name", "language__name", "lesson_type__name", "is_active")
