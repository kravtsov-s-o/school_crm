from pricing.models import SchoolPrice, SchoolPriceRow
from pricing.serializers.admin.base_price import PriceAdminBaseSerializer, PriceRowBaseSerializer


class SchoolPriceRowSerializer(PriceRowBaseSerializer):
    """A row of the school price grid."""

    class Meta(PriceRowBaseSerializer.Meta):
        model = SchoolPriceRow


class SchoolPriceAdminListSerializer(PriceAdminBaseSerializer):
    """Compact school price for the admin list (no rows)."""

    class Meta:
        model = SchoolPrice
        fields = ("id", "name", "currency", "language", "lesson_type", "is_active")


class SchoolPriceAdminSerializer(SchoolPriceAdminListSerializer):
    """School price with its full rows grid (create/update)."""

    rows = SchoolPriceRowSerializer(many=True)

    class Meta(SchoolPriceAdminListSerializer.Meta):
        fields = (*SchoolPriceAdminListSerializer.Meta.fields, "rows")
        read_only_fields = ("id",)
