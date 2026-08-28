from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from school_settings.models import ExchangeRate
from school_settings.serializers.admin.exchange_rate import ExchangeRateAdminSerializer


@extend_schema(tags=["Admin: Exchange Rate"])
class ExchangeRateAdminViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only exchange rates (list/retrieve). Populated by the ``fetch_rates``
    NBU job, not edited by hand."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = ExchangeRateAdminSerializer
    queryset = ExchangeRate.objects.all()
