from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from finance.filters import TransactionFilter
from finance.models import Transaction
from finance.serializers.admin.transaction import TransactionAdminSerializer


@extend_schema(tags=["Admin: Transaction"])
class TransactionAdminViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                              mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Admin ledger for transactions — create (manual codes only) + list/retrieve.
    Append-only: no update/delete. Amount is sent positive and signed by the
    transaction direction on save."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = TransactionAdminSerializer
    queryset = Transaction.objects.select_related("account", "currency", "lesson")
    filterset_class = TransactionFilter
    search_fields = (
        "comment",
        "account__student_profile__user__first_name",
        "account__student_profile__user__last_name",
        "account__teacher_profile__user__first_name",
        "account__teacher_profile__user__last_name",
        "account__company__name",
    )
    ordering_fields = ("date", "type", "currency__code")
