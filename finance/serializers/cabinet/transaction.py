from rest_framework import serializers

from finance.models import Transaction
from school_settings.serializers.common import CurrencyBriefSerializer


class TransactionCabinetSerializer(serializers.ModelSerializer):
    """Read-only transaction for the owner's own ledger (no account ref — it's theirs)."""

    currency = CurrencyBriefSerializer(read_only=True)
    lesson = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ("id", "date", "type", "amount", "currency", "lesson", "comment")
        read_only_fields = fields
