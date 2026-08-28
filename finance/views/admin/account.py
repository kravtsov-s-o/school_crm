from decimal import Decimal

from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from finance.models import Account
from finance.serializers.admin.account import AccountAdminSerializer


@extend_schema(tags=["Admin: Account"])
class AccountAdminViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only accounts overview — owner + derived balance (annotated). Accounts
    are created with their profile/company, never edited directly here."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = AccountAdminSerializer
    queryset = (Account.objects
                .select_related("student_profile__user", "teacher_profile__user", "company")
                .annotate(total_balance=Coalesce(Sum("transactions__amount"), Decimal(0))))
