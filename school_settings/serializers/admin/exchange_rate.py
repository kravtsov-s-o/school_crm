from rest_framework import serializers

from school_settings.models import ExchangeRate
from school_settings.serializers.common import CurrencyBriefSerializer


class ExchangeRateAdminSerializer(serializers.ModelSerializer):
    """Read-only exchange rate — currency ref + rate on a date."""

    currency = CurrencyBriefSerializer(read_only=True)

    class Meta:
        model = ExchangeRate
        fields = ("id", "currency", "rate", "date")
        read_only_fields = ("id",)