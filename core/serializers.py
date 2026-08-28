from decimal import Decimal

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class BalanceSerializerMixin(serializers.Serializer):
    """Adds a read-only ``balance`` field — the linked Account's balance, or 0."""
    balance = serializers.SerializerMethodField()

    @extend_schema_field(serializers.DecimalField(max_digits=12, decimal_places=2))
    def get_balance(self, obj) -> Decimal:
        return obj.account.balance if obj.account_id else Decimal("0.00")


class BriefRelatedField(serializers.PrimaryKeyRelatedField):
    """Accept a PK on write; returns the brief serializer's dict on read."""

    def __init__(self, brief_serializer, **kwargs):
        self.brief_serializer = brief_serializer
        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        return self.brief_serializer(value).data

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}
        if cutoff is not None:
            queryset = queryset[:cutoff]
        return {item.pk: self.display_value(item) for item in queryset}
