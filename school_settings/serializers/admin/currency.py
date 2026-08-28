from rest_framework import serializers

from school_settings.models import Currency


class CurrencyAdminSerializer(serializers.ModelSerializer):
    """Admin CRUD for a currency; ``is_system`` is exposed but frozen (read-only)."""

    class Meta:
        model = Currency
        fields = ("id", "code", "name", "symbol", "is_active", "is_system")
        read_only_fields = ("id", "is_system")
