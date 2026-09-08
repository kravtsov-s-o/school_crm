from core.serializers import BriefRelatedField
from pricing.models import TeacherRate, TeacherRateRow
from pricing.serializers.admin.base_price import PriceAdminBaseSerializer, PriceRowBaseSerializer
from school_settings.models import TeacherGrade
from school_settings.serializers.common import TeacherGradeBriefSerializer


class TeacherRateRowSerializer(PriceRowBaseSerializer):
    """A row of a teacher rate."""

    class Meta(PriceRowBaseSerializer.Meta):
        model = TeacherRateRow


class TeacherRateAdminListSerializer(PriceAdminBaseSerializer):
    """Compact teacher rate for the admin list (no rows); adds grade."""

    grade = BriefRelatedField(TeacherGradeBriefSerializer, queryset=TeacherGrade.objects.all())

    class Meta:
        model = TeacherRate
        fields = ("id", "name", "currency", "language",
                  "lesson_type", "grade", "is_active")


class TeacherRateAdminSerializer(TeacherRateAdminListSerializer):
    """Teacher rate with its full rows grid (create/update)."""

    rows = TeacherRateRowSerializer(many=True)

    class Meta(TeacherRateAdminListSerializer.Meta):
        model = TeacherRate
        fields = (*TeacherRateAdminListSerializer.Meta.fields, "rows")
        read_only_fields = ("id",)
