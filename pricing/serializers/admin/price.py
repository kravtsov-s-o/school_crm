from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.serializers import BriefRelatedField
from pricing.models import (
    PersonalPlan,
    PersonalPlanRow,
    SchoolPrice,
    SchoolPriceRow,
    TeacherRate,
    TeacherRateRow,
)
from school_settings.models import Currency, Duration, Language, LessonType, TeacherGrade
from school_settings.serializers.common import (
    CurrencyBriefSerializer,
    DurationBriefSerializer,
    LanguageBriefSerializer,
    LessonTypeBriefSerializer,
    TeacherGradeBriefSerializer,
)


class PriceRowBaseSerializer(serializers.ModelSerializer):
    duration = BriefRelatedField(DurationBriefSerializer, queryset=Duration.objects.all())

    class Meta:
        fields = ("duration", "amount")


class SchoolPriceRowSerializer(PriceRowBaseSerializer):
    class Meta(PriceRowBaseSerializer.Meta):
        model = SchoolPriceRow


class TeacherRateRowSerializer(PriceRowBaseSerializer):
    class Meta(PriceRowBaseSerializer.Meta):
        model = TeacherRateRow


class PersonalPlanRowSerializer(PriceRowBaseSerializer):
    class Meta(PriceRowBaseSerializer.Meta):
        model = PersonalPlanRow


class PriceAdminBaseSerializer(serializers.ModelSerializer):
    currency = BriefRelatedField(CurrencyBriefSerializer, queryset=Currency.objects.all())
    language = BriefRelatedField(LanguageBriefSerializer, queryset=Language.objects.all())
    lesson_type = BriefRelatedField(LessonTypeBriefSerializer, queryset=LessonType.objects.all())

    def validate(self, attrs):
        rows = attrs.get("rows")
        if rows:
            durations = [row["duration"] for row in rows]
            if len(durations) != len(set(durations)):
                raise serializers.ValidationError(
                    {"rows": _("Duplicate duration in rows.")}
                )
        return attrs

    def _sync_rows(self, plan, rows):
        plan.rows.all().delete()
        RowModel = plan.rows.model
        RowModel.objects.bulk_create([RowModel(plan=plan, **row) for row in rows])

    @transaction.atomic
    def create(self, validated_data):
        rows = validated_data.pop("rows", [])
        plan = super().create(validated_data)
        self._sync_rows(plan, rows)
        return plan

    @transaction.atomic
    def update(self, instance, validated_data):
        rows = validated_data.pop("rows", None)
        plan = super().update(instance, validated_data)
        if rows is not None:
            self._sync_rows(plan, rows)
        return plan


class SchoolPriceAdminSerializer(PriceAdminBaseSerializer):
    rows = SchoolPriceRowSerializer(many=True)

    class Meta:
        model = SchoolPrice
        fields = ("id", "name", "currency", "language", "lesson_type", "is_active", "rows")
        read_only_fields = ("id",)


class TeacherRateAdminSerializer(PriceAdminBaseSerializer):
    rows = TeacherRateRowSerializer(many=True)
    grade = BriefRelatedField(TeacherGradeBriefSerializer, queryset=TeacherGrade.objects.all())

    class Meta:
        model = TeacherRate
        fields = ("id", "name", "currency", "language",
                  "lesson_type", "grade", "is_active", "rows")
        read_only_fields = ("id",)


class PersonalPlanAdminSerializer(PriceAdminBaseSerializer):
    rows = PersonalPlanRowSerializer(many=True)

    class Meta:
        model = PersonalPlan
        fields = ("id", "name", "currency", "language", "lesson_type", "is_active", "rows")
        read_only_fields = ("id",)
