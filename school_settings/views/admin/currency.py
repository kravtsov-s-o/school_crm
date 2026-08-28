from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions

from school_settings.models import Currency
from school_settings.serializers.admin.currency import CurrencyAdminSerializer


@extend_schema(tags=["Admin: Currency"])
class CurrencyAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for currencies. System records can't be deleted (403) or
    re-flagged (400), enforced by ``SystemRecordMixin`` + the exception handler."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = CurrencyAdminSerializer
    queryset = Currency.objects.all()