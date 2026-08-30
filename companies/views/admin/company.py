from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import Coalesce
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from companies.models import Company
from companies.serializers.admin.company import CompanyAdminSerializer


@extend_schema(tags=["Admin: Company"])
class CompanyAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for companies."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = CompanyAdminSerializer
    queryset = (Company.objects
                .select_related("currency", "account")
                .prefetch_related("personal_plans")
                .annotate(balance=Coalesce(Sum("account__transactions__amount"), Decimal(0)))
                .order_by("name")
                .distinct())
    filterset_fields = ("currency", "is_active", "personal_plans")
    search_fields = ("name",)
    ordering_fields = ("name", "balance", "coverage_percent")
