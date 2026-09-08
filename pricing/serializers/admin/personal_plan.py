from pricing.models import PersonalPlan, PersonalPlanRow
from pricing.serializers.admin.base_price import PriceAdminBaseSerializer, PriceRowBaseSerializer


class PersonalPlanRowSerializer(PriceRowBaseSerializer):
    """A row of a personal plan."""

    class Meta(PriceRowBaseSerializer.Meta):
        model = PersonalPlanRow


class PersonalPlanAdminListSerializer(PriceAdminBaseSerializer):
    """Compact personal plan for the admin list (no rows)."""

    class Meta:
        model = PersonalPlan
        fields = ("id", "name", "currency", "language", "lesson_type", "is_active")


class PersonalPlanAdminSerializer(PersonalPlanAdminListSerializer):
    """Personal plan with its full rows grid (create/update)."""

    rows = PersonalPlanRowSerializer(many=True)

    class Meta(PersonalPlanAdminListSerializer.Meta):
        model = PersonalPlan
        fields = (*PersonalPlanAdminListSerializer.Meta.fields, "rows")
        read_only_fields = ("id",)
